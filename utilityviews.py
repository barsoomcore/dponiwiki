from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.views import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime, urllib2
from tagging.models import Tag, TaggedItem

from dponisetting.dponiwiki.models import Island, IslandComponent, ChangeSet
from dponisetting.dponiwiki.forms import UserCreationFormExtended

def canonical(request, canonicity):
	'''	Returns a list of islands matching the supplied canonicity '''
	
	if canonicity == "True":
		canonicity = "Canonical"
		island_list = Island.objects.filter(iscanonical__exact=True).order_by('name')
	else:
		canonicity = "Non-Canonical"
		island_list = Island.objects.filter(iscanonical__exact=False).order_by('name')
	
	heading = 'Some islands to explore...'
	
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	
	paginator = Paginator(island_list, 25)

	try:
		islands = paginator.page(page)
	except (EmptyPage, InvalidPage):
		islands = paginator.page(paginator.num_pages)
	
	template_params = { 'heading': heading, 'islands': islands, 'canonicity': canonicity }
	return render_to_response(
		"templates/island_list.html", 
		template_params, 
		context_instance=(RequestContext(request))
	)

	
def search(request, type):
	''' Returns a list of either islands or components based on search string '''
	if 'q' in request.GET:
		term = request.GET['q']
		
		try:
			class_type = globals()[type]
		except KeyError:
			return HttpResponseNotFound
		
		try:
			page = int(request.GET.get('page', '1'))
		except ValueError:
			page = 1
		
		islands = ''
		components = ''
		
		if class_type == Island:
			island_list = class_type.objects.filter(Q(name__icontains=term) | Q(summary__icontains=term))
			url = "templates/island_list.html"
			paginator = Paginator(island_list, 25)
		
			try:
				islands = paginator.page(page)
			except (EmptyPage, InvalidPage):
				islands = paginator.page(paginator.num_pages)
				
		elif class_type == IslandComponent:
			component_list = class_type.objects.filter(Q(name__contains=term) | Q(content__contains=term))
			url = "templates/island_list.html"
			type = "Island Component"
			paginator = Paginator(component_list, 25)
		
			try:
				components = paginator.page(page)
			except (EmptyPage, InvalidPage):
				components = paginator.page(paginator.num_pages)
		
		heading = "Search Results: All " + type + "s containing the term \"" + term + "\""
		
		template_params = { 
			'heading': heading, 
			'islands': islands, 
			'components': components, 
			'term': term 
			}
			
	return render_to_response(url, template_params, context_instance=(RequestContext(request)))


def by_user(request, user=None):
	''' Returns both islands and components owned by supplied user. '''
	if 'q' in request.GET:
		owner = request.GET['q']
	elif user:
		owner = user
		
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	
	# this whole bit seems retarded to me but things keep barfing if I don't set
	# the relevant bits to '' ahead of time.
	
	island_list = Island.objects.filter(owner__username__exact=owner)
	component_list = IslandComponent.objects.filter(owner__username__exact=owner)
	all_list = island_list
	
	island_paginator = Paginator(island_list, 15)
	component_paginator = Paginator(component_list, 15)
	try:
		islands = island_paginator.page(page)
		components = component_paginator.page(page)
	except (EmptyPage, InvalidPage):
		islands = island_paginator.page(island_paginator.num_pages)
		components = component_paginator.page(component_paginator.num_pages)
	island_header = ''
	component_header = ''
	conjunction = ''
	if island_list:
		island_header = "Islands"
	if component_list:
		component_header = "Components"
	if component_header and island_header:
		conjunction = " and "
	
	if not component_header and not island_header:
		heading = owner + " hasn't created any islands or components yet."
	else:
		heading = "All " + island_header + conjunction + component_header + " Owned By \"" + owner + "\""
	
	template_params = {
		'heading': heading, 
		'islands': islands, 
		'components': components, 
		'term': owner
		}
	
	return render_to_response(
		'templates/island_list.html', 
		template_params, 
		context_instance=(RequestContext(request))
		)


def by_tags(request, url):
	'''parses request, spits out tags, finds components'''
	tag_name_list = url.split('/')
	tag_list = []
	for tag in tag_name_list:
		tagged_item = get_object_or_404(Tag, name=tag)
		if tagged_item not in tag_list:
			tag_list.append(tagged_item)
	tagged_items = TaggedItem.objects.get_by_model(IslandComponent, tag_list)
	
	item_paginator = Paginator(tagged_items, 25)
	
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	
	try:
		components = item_paginator.page(page)
	except (EmptyPage, InvalidPage):
		components = item_paginator.page(item_paginator.num_pages)
	
	template_params = {'components': components, 'tags': tag_list, }
	
	return render_to_response(
		'templates/islandcomponent_list.html', 
		template_params,
		context_instance=(RequestContext(request))
		)

def item_history(request, slug, type):
	''' Display changeset list for given item. '''
	if request.method == 'GET':
		
		try:
			class_type = globals()[type]
		except KeyError:
			return HttpResponseRedirect('/dponiwiki/')

		item = get_object_or_404(class_type, slug=slug)
		changes_list = item.changeset_set.all().order_by('-revision')
		paginator = Paginator(changes_list, 25)
		
		try:
			page = int(request.GET.get('page', '1'))
		except ValueError:
			page = 1
		
		try:
			changes = paginator.page(page)
		except (EmptyPage, InvalidPage):
			changes = paginator.page(paginator.num_pages)
		
		template_params = {'item': item,
                           'changes': changes,
                           	'type': type}

		return render_to_response('templates/history.html',
                                  template_params, 
                                  context_instance=(RequestContext(request))
                                  )

	return HttpResponseNotAllowed(['GET'])

@login_required
def revert_to_revision(request, slug, type):
	''' Reverts the current item to the selected revision. '''
	if request.method == 'POST':
		
		try:
			class_type = globals()[type]
		except KeyError:
			return HttpResponseRedirect('/dponiwiki/')

		item = get_object_or_404(class_type, slug=slug)

		revision = int(request.POST['revision'])

		item.revert_to(revision, request.user)
        
        # obviously this is a terrible solution
        
		url = '/dponiwiki/' + type + '/history/' + slug
        
		return HttpResponseRedirect(url)

	return HttpResponseNotAllowed(['GET'])


def view_changeset(request, type, slug, revision, *args, **kw):
	''' Returns the diff-ed version of the item. '''
	if request.method == "GET":
    
		# no idea why this is being done this way
		# don't really know what's happening so leave it until I have time to review

		component_args = {'component__slug': slug}

		changeset = get_object_or_404(
            ChangeSet.objects.all().select_related(),
            revision=int(revision),
            **component_args)

		component = changeset.component

		template_params = {'component': component,
                           'component_name': component.name,
                           'changeset': changeset,
                           'slug': slug,
                           'type': type}
		
		return render_to_response('templates/changeset.html',
                                  template_params,
                                  context_instance=RequestContext(request))
	
	return HttpResponseNotAllowed(['GET'])
    
    
def register(request):
	
	if request.method == 'POST':
		form = UserCreationFormExtended(data=request.POST)
		if form.is_valid():
			new_user = form.save()			
			user = authenticate(username=new_user.username, password=form.cleaned_data['password1'])
			if user is not None:
				login(request, user)
			return HttpResponseRedirect(reverse('homepage'))
	else: form = UserCreationFormExtended()
		
	return render_to_response(
		'templates/registration/registration_form.html', 
		{ 'form' : form }, 
		context_instance=RequestContext(request)
		)

def villain_picker(request, villain=None, level='0'):

	skills = open(settings.ROLES_URL + 'Skills.data')
	if skills:
		skill_list = skills.readlines()
	villain_data = []
	villain_skills = []
	if villain:
		villain_stats = open(settings.ROLES_URL + villain + '.data')
		if villain_stats:
			villain_lines = villain_stats.readlines()
		if villain_lines:
			for line in villain_lines:
				line = line.rstrip('\n')
				line = line.split('|')
				villain_data.append(line)
		if skills:
			villain_skills_names = villain_data[1][16].split(', ')
			for skill in villain_skills_names:
				skill_entry = []
				skill_entry.append(skill)
				for item in skill_list:
					item = item.rstrip('\n')
					item = item.split('|')
					if item[0] == skill:
						skill_entry.append(item[1])
				villain_skills.append(skill_entry)
	
	
	if villain == "WarLeader":
		villain = "War Leader"
		
	try:
		level = int(level)
		if 1 > level or level > 20:
			level = '0'
	except ValueError:
		level = '0'

	template_params = {'villain_data': villain_data,
						'villain_skills': villain_skills,
						'villain_name': villain,
						'villain_level': level}

	return render_to_response('templates/villain.html', template_params, 
								context_instance=RequestContext(request))