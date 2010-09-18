from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import datetime
from tagging.models import Tag, TaggedItem

from dponisetting.dponiwiki.models import Island, IslandComponent, ChangeSet
from dponisetting.dponiwiki.forms import UserCreationFormExtended


def paginate(request, input_list, per_page=25):
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	paginator = Paginator(input_list, per_page)
	
	try:
		return_list = paginator.page(page)
	except (EmptyPage, InvalidPage):
		return_list = paginator.page(paginator.num_pages)
	
	return return_list


def canonical(request, canonicity):
	'''	Returns a list of islands matching the supplied canonicity '''
	
	if canonicity == "True":
		canonicity = "Canonical"
		island_list = Island.objects.filter(iscanonical__exact=True).order_by('name')
	else:
		canonicity = "Non-Canonical"
		island_list = Island.objects.filter(iscanonical__exact=False).order_by('name')
	
	heading = 'Some islands to explore...'
	
	islands = paginate(request, island_list)
	
	template_params = { 
		'heading': heading, 
		'islands': islands, 
		'canonicity': canonicity 
	}
	
	return render_to_response(
		"templates/island_list.html", 
		template_params, 
		context_instance=(RequestContext(request))
	)

	
def search(request, type):
	''' Returns a list of either islands or components based on search string '''
	heading = 'Nothing found to match that.'
	islands = ''
	components = ''
	term = ''
	
	if 'q' in request.GET:
		term = request.GET['q']
	
	if term:		
		try:
			class_type = globals()[type]
		except KeyError:
			return HttpResponseNotFound
		
		if class_type == Island:
			island_list = class_type.objects.filter(Q(name__icontains=term) | Q(summary__icontains=term))
			
			islands = paginate(request, island_list)
			
			if islands.object_list:
				heading = "Search Results: All Islands containing the term \"" + term + "\""
							
		elif class_type == IslandComponent:
			component_list = class_type.objects.filter(Q(name__contains=term) | Q(content__contains=term))
			
			components = paginate(request, component_list)
			
			if components.object_list:
				heading = "Search Results: All Island Components containing the term \"" + term + "\""
			
	template_params = { 
		'heading': heading, 
		'islands': islands, 
		'components': components, 
		'term': term 
	}
			
	return render_to_response(
		"templates/island_list.html", 
		template_params, 
		context_instance=(RequestContext(request))
	)


def by_owner(request, owner=None):
	''' Returns both islands and components owned by supplied user. '''
	
	heading = 'Nothing found to match that'
	islands = ''
	components = ''
	if 'q' in request.GET:
		owner = request.GET['q']
	
	if owner:
		island_list = Island.objects.filter(owner__username__exact=owner)
		component_list = IslandComponent.objects.filter(owner__username__exact=owner)
		
		islands = paginate(request, island_list, 15)
		components = paginate(request, component_list, 15)
		
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
	
	components = paginate(request, tagged_items)
	
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
		
		changes = paginate(request, changes_list)
		
		template_params = {'item': item,
                           'changes': changes,
                           	'type': type
        }

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
		
		return HttpResponseRedirect(reverse(
			'item_history', 
			kwargs={ 'type': type, 'slug': slug }
		))

	return HttpResponseNotAllowed(['GET'])


def view_changeset(request, type, slug, revision, *args, **kw):
	''' Returns the diff-ed version of the item. '''
	if request.method == "GET":

		component_args = {'component__slug': slug}

		changeset = get_object_or_404(
            ChangeSet.objects.all().select_related(),
            revision=int(revision),
            **component_args)

		component = changeset.component

		template_params = {'component': component,
                           'changeset': changeset,
                           'type': type
        }
		
		return render_to_response('templates/changeset.html',
                                  template_params,
                                  context_instance=RequestContext(request)
        )
	
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