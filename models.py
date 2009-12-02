from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.db.models import permalink
import datetime
import re
from django.template.defaultfilters import slugify
from django.db.models.query import QuerySet
from django.db.models.signals import post_save

from tagging.fields import TagField
from tagging.models import Tag

from wiki.utils import get_ct
from wiki.models import diff, QuerySetManager, NonRemovedArticleManager, NonRevertedChangeSetManager

# Google Diff Match Patch library
# http://code.google.com/p/google-diff-match-patch
from diff_match_patch import diff_match_patch

# We dont need to create a new one everytime
dmp = diff_match_patch()


class WikiComponent(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 100, unique=True)
	owner = models.ForeignKey(User)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True, blank=True)
	modified = models.DateTimeField(auto_now=True, blank=True)
	comment = models.CharField(max_length=50)
	
	def __unicode__(self):
		return u'%s' % (self.name)
	
	def save(self):
		
		latest_comment = self.comment
		self.comment = ''
        
        # code below from:
        # http://www.revolunet.com/snippets/snippet/automatic-and-unique-slug-field
		if not self.slug:
			self.slug = slugify(self.name) 
		
		while True:
			try:
				super(WikiComponent, self).save()
			except IntegrityError:
				matches = re.match(r'^(.*)-(\d+)$', self.slug)
				if matches:
					current = int(matches .group(2)) + 1
					self.slug = matches .group(1) + '-' + str(current)
				else:
					self.slug += '-2'
			else:
				break
		#
		#
		
		# prep the new revision
		this_change = self.new_revision(
			self.content, 
			self.name, 
			latest_comment, 
			self.owner
		)
		this_change.save()

# the next batch of functions are taken from the Wiki-App project
	def latest_changeset(self):
		try:
			return self.changeset_set.filter(
				reverted=False).order_by('-revision')[0]
		except IndexError:
			return ChangeSet.objects.none()

	def new_revision(self, old_content, old_name, comment, owner):
		'''Create a new ChangeSet with the old content.'''

		content_diff = diff(self.content, old_content)

		cs = ChangeSet.objects.create(
			component=self,
			owner=owner,
			comment=comment,
			old_name=old_name,
			content_diff=content_diff)

#		if None not in (notification, self.owner):
#			notification.send([self.owner], "wiki_article_edited",
#						{'article': self, 'user': owner})

		return cs

	def revert_to(self, revision, owner=None):
		""" Revert the article to a previuos state, by revision number.
		"""
		changeset = self.changeset_set.get(revision=revision)
		changeset.reapply(owner)

		
class IslandComponent(WikiComponent):
	
	def host_islands_list(self):
		host_island_objects = self.host_islands.all()
		island_names = ""
		if host_island_objects:
			island_names = host_island_objects[0].name
			for object in host_island_objects[1:]:
				island_names = island_names + ", " + object.name
		return island_names
	
	class Meta:
		ordering = ['modified']
	
	@permalink
	def get_absolute_url(self):
		return("component-detail", (), {'slug': self.slug})

class Island(WikiComponent):
	summary = models.TextField(blank=True)
	components = models.ManyToManyField(IslandComponent, related_name='host_islands',blank=True)
	iscanonical = models.BooleanField(default=True, blank=True)
	
	class Meta:
		ordering = ['modified']
	
	@permalink
	def get_absolute_url(self):
		return('island-detail', (), {'slug': self.slug})

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
		ordering = ('-revision',)

	def __unicode__(self):
		return u'#%s' % self.revision

	@models.permalink
	def get_absolute_url(self):
		return ('wiki_changeset', (),
                {'slug': self.component.slug,
                 'name': self.component.name,
                 'revision': self.revision})


	def is_anonymous_change(self):
		return self.editor is None

	def reapply(self, editor_ip, editor):
		""" Return the component to this revision.
        """

		# XXX Would be better to exclude reverted revisions
		#     and revisions previous/next to reverted ones
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
		old_title = component.title
		old_markup = component.markup

		component.content = content
		component.title = changeset.old_title
		component.markup = changeset.old_markup
		component.save()

		component.new_revision(
			old_content=old_content, old_title=old_title,
			old_markup=old_markup,
			comment="Reverted to revision #%s" % self.revision)

		self.save()

		if None not in (notification, self.owner):
			notification.send([self.owner], "wiki_revision_reverted",
                              {'revision': self, 'component': self.component})

	def save(self, force_insert=False, force_update=False):
		""" Saves the component with a new revision.
		"""
		if self.id is None:
			try:
				self.revision = ChangeSet.objects.filter(
					component=self.component).latest().revision + 1
			except self.DoesNotExist:
				self.revision = 1
		super(ChangeSet, self).save(force_insert, force_update)

	def display_diff(self):
		''' Returns a HTML representation of the diff.
		'''

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