import datetime
import re
import operator

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import models, IntegrityError
from django.db.models import permalink
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from tagging.fields import TagField
from tagging.models import Tag
from autoslug.fields import AutoSlugField

from dponisetting import settings

# Google Diff Match Patch library
# http://code.google.com/p/google-diff-match-patch
from diff_match_patch import diff_match_patch

# following batch of models taken from wiki-app

# We dont need to create a new one everytime
dmp = diff_match_patch()

def diff(txt1, txt2):
	"""Create a 'diff' from txt1 to txt2."""
	patch = dmp.patch_make(txt1, txt2)
	return dmp.patch_toText(patch)

# Avoid boilerplate defining our own querysets
class QuerySetManager(models.Manager):
	def get_query_set(self):
		return self.model.QuerySet(self.model)

class NonRevertedChangeSetManager(QuerySetManager):
	def get_default_queryset(self):
		super(NonRevertedChangeSetManager, self).get_query_set().filter(
				reverted=False)

# thanks to the wiki-app crew for those items!

class StaticPage(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 100, unique=True)
	owner = models.ForeignKey(User)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	
	@permalink
	def get_absolute_url(self):
		return('page-detail', (), {'slug': self.slug})

class WikiComponent(models.Model):
	name = models.CharField(max_length = 100)
	slug = AutoSlugField(populate_from='name', unique=True, editable=False)
	owner = models.ForeignKey(User, editable=False)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True, blank=True)
	modified = models.DateTimeField(auto_now=True, blank=True)
	comment = models.CharField(max_length=50)
	
	class Meta:
		ordering = ['-modified']
	
	def __unicode__(self):
		return u'%s' % (self.name)
	
	def save(self, editor=None, latest_comment=None, *args, **kwargs):
	
		if not editor:
			editor = self.owner
	
		# first capture data from the previous version so as to make revisions possible

		try:
			old_version = WikiComponent.objects.filter(slug= self.slug)[0]
			old_content = old_version.content
		except IndexError:
			old_content = ''
		
		# clear out self.comment so next time we edit this component, the comment field
		# is empty
		
		if latest_comment == None:
			latest_comment = self.comment
		self.comment = ''
		latest_comment = latest_comment[0:49]
		
		# now we want to reset the order of the components so the values don't keep getting bigger
		
		current_order = ComponentOrder.objects.filter(island__exact=self).order_by('order')
		
		for index, item in enumerate(current_order):
			item.order = index
			item.save()
		
		super(WikiComponent, self).save(*args, **kwargs)
		
		try:
			latest_change = ChangeSet.objects.filter(component=self).order_by('-revision')[0]
			new_revision_number = latest_change.revision+1
		except IndexError:
			new_revision_number = 1
		
		# prep the new revision
		this_change = self.new_revision(
			old_content, 
			self.name, 
			latest_comment, 
			editor,
			new_revision_number
		)
		this_change.save()

	# the next batch of functions are taken from the Wiki-App project
	def latest_changeset(self):
		try:
			return self.changeset_set.filter(
				reverted=False).order_by('-revision')[0]
		except IndexError:
			return ChangeSet.objects.none()

	def new_revision(self, old_content, old_name, comment, owner, revision):
		'''Create a new ChangeSet with the old content.'''
		
		content_diff = diff(self.content, old_content)

		cs = ChangeSet.objects.create(
			component=self,
			owner=owner,
			comment=comment,
			old_name=old_name,
			revision=revision,
			content_diff=content_diff)

		return cs

	def revert_to(self, revision, owner=None):
		""" Revert the article to a previous state, by revision number."""
		changeset = self.changeset_set.get(revision=revision)
		changeset.reapply(owner)
		

class Island(WikiComponent):
	summary = models.TextField(blank=True)
	components = models.ManyToManyField(
		'IslandComponent', 
		related_name='host_islands',
		blank=True, 
		through='ComponentOrder'
	)
	iscanonical = models.BooleanField(default=False, blank=True)
	
	def get_unique_tags(self):
		components = self.components.all()
		tags = []
		for component in components:
			component_tags = Tag.objects.get_for_object(component)
			for tag in component_tags:
			 	tags.append(tag.name)
		return set(tags) & set(settings.COMPONENT_TAGS)
		
	def get_ordered_components(self):
		components = self.components.all()
		ordered_components = []
		for component in components:
			order = ComponentOrder.objects.filter(island__exact=self, component__exact=component)[0]
			setattr(component, 'order', order.order)
			ordered_components.append(component)
		ordered_components.sort(key=operator.attrgetter('order'))
		return ordered_components
	
	def get_reorder_list(self):
		reorder_list = {}
		if len(self.get_ordered_components()) > 1:
			for component in self.get_ordered_components():
				reorder_list[component.order] = component.name[0:12]
		return sorted(reorder_list.items())
	
	@permalink
	def get_absolute_url(self):
		return('island-detail', (), {'slug': self.slug})

		
class IslandComponent(WikiComponent):

	tags = TagField()
	is_box = models.BooleanField(default=False)
	
	def host_islands_list(self):
		''' This function is used in admin.py to populate the host islands for a
		component in the admin interface.'''
		host_island_objects = self.host_islands.all()
		island_names = ""
		if host_island_objects:
			island_names = host_island_objects[0].name
			for object in host_island_objects[1:]:
				island_names = island_names + ", " + object.name
		return island_names
	
	def add_component_to_end(self, editor=None, island=None):
		current_order = ComponentOrder.objects.filter(island__exact=island).order_by('order')
		new_order_order = 1
		if current_order:
			if self not in island.components.all():
				for item in current_order:
					if item.order == new_order_order:
						new_order_order = new_order_order + 1
		
		new_order = ComponentOrder(island=island, component=self, order=new_order_order)
		new_order.save()
		island.save(latest_comment="Added Component " + self.name, editor=editor)
	
	def save(self, editor=None, *args, **kwargs):
		try:
			host_islands = self.host_islands.all()
		except ValueError:
			host_islands = []
		latest_changeset = self.latest_changeset()
		for host_island in host_islands:
			host_island.save(
				latest_comment="Updated " + self.name + ": " + latest_changeset.comment, 
				editor=editor
			)
		super(IslandComponent, self).save(*args, **kwargs)
	
	@permalink
	def get_absolute_url(self):
		return("component-detail", (), {'slug': self.slug})

class ComponentOrder(models.Model):
	island = models.ForeignKey(Island)
	component = models.ForeignKey(IslandComponent)
	order = models.IntegerField()


# Model below taken from Wiki-App

class ChangeSet(models.Model):
	"""A report of an older version of some component."""

	component = models.ForeignKey(WikiComponent)

	# Editor identification -- logged or anonymous
	owner = models.ForeignKey(User, null=True, related_name='editor')

	# Revision number, starting from 1
	revision = models.IntegerField()

	# How to recreate this version
	old_name = models.CharField(max_length=100)
	content_diff = models.TextField(blank=True)
	comment = models.CharField(max_length=50, blank=True)
	modified = models.DateTimeField(auto_now=True)
	reverted = models.BooleanField(default=False)
	objects = QuerySetManager()
	non_reverted_objects = NonRevertedChangeSetManager()

	class QuerySet(QuerySet):
		def all_later(self, revision):
			""" Return all changes later to the given revision.
			Util when we want to revert to the given revision.
			"""
			return self.filter(revision__gt=int(revision))

	class Meta:
		get_latest_by  = 'modified'
		
		# doesn't seem like this is getting used properly
		
		ordering = ('-revision',)

	def __unicode__(self):
		return u'#%s' % self.revision

	@permalink
	def get_absolute_url(self):
		source_item = Island.objects.filter(slug=self.component.slug)
		if not source_item:
			source_item = IslandComponent.objects.filter(slug=self.component.slug)
		type = source_item[0].__class__.__name__
		return (
			'wiki_changeset', 
			(), 
			{
				'type': type, 
				'slug': self.component.slug, 
				'revision': self.revision
			}
		)


	def is_anonymous_change(self):
		return self.editor is None

	def reapply(self, editor):
		""" Return the component to this revision."""

		# XXX Would be better to exclude reverted revisions
		#     and revisions previous/next to reverted ones
		# curious we don't use QuerySet.all_later as defined above
		
		next_changes = self.component.changeset_set.filter(
			revision__gt=self.revision).order_by('-revision')

		component = self.component

		content = None
		for changeset in next_changes:
			if content is None:
				content = component.content
			patch = dmp.patch_fromText(changeset.content_diff)
			content = dmp.patch_apply(patch, content)[0]

			changeset.reverted = True
			changeset.save()

		old_content = component.content
		old_name = component.name

		component.content = content
		component.name = changeset.old_name
		component.save(latest_comment="Reverted to revision #%s" % self.revision, editor=editor)

		self.save()

	def save(self, force_insert=False, force_update=False, *args, **kwargs):
		""" Saves the component with a new revision."""
		
		if self.id is None:
			try:
				latest_revision = ChangeSet.objects.filter(
					component=self.component).order_by('-revision')[0]
				self.revision = latest_revision.revision + 1
			except IndexError:
				self.revision = 1
		super(ChangeSet, self).save(force_insert, force_update, *args, **kwargs)

	def display_diff(self):
		''' Returns a HTML representation of the diff.'''

		# well, it *will* be the old content
		old_content = self.component.content

		# newer non-reverted revisions of this component, starting from this
		newer_changesets = ChangeSet.non_reverted_objects.filter(
			component=self.component,
			revision__gte=self.revision)

		# apply all patches to get the content of this revision
		for i, changeset in enumerate(newer_changesets):
			patches = dmp.patch_fromText(changeset.content_diff)
			if len(newer_changesets) == i+1:
				# we need to compare with the next revision after the change
				next_rev_content = old_content
			old_content = dmp.patch_apply(patches, old_content)[0]

		diffs = dmp.diff_main(old_content, next_rev_content)
		return dmp.diff_prettyHtml(diffs)

