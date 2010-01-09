from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout

from dponisetting.dponiwiki.models import Island, IslandComponent, ChangeSet
from dponisetting.dponiwiki.forms import UserCreationFormExtended

def canonical(request, canonicity):
	island_list = Island.objects.filter(iscanonical=canonicity)
	if canonicity == "True":
		heading = "Canonical Islands"
	else:
		heading = "Non-Canonical Islands"
	return render_to_response("templates/island_list.html", locals(), context_instance=(RequestContext(request)))

	
def search(request, type):
	if 'q' in request.GET:
		term = request.GET['q']
		
		try:
			class_type = globals()[type]
		except KeyError:
			return HttpResponseRedirect('/dponiwiki/')
		
		if class_type == Island:
			island_list = class_type.objects.filter(Q(name__contains=term) | Q(summary__contains=term))
			url = "templates/island_list.html"
		elif class_type == IslandComponent:
			component_list = class_type.objects.filter(Q(name__contains=term) | Q(content__contains=term))
			url = "templates/islandcomponent_list.html"
			type = "Island Component"
		
		heading = "Search Results: All " + type + "s containing the term \"" + term + "\""
			
	return render_to_response(url, locals(), context_instance=(RequestContext(request)))


def by_user(request, user=None):
	if 'q' in request.GET:
		owner = request.GET['q']
	elif user:
		owner = user
		
	island_list = Island.objects.filter(owner__username__exact=owner)
	component_list = IslandComponent.objects.filter(owner__username__exact=owner)
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
	
	template_params = {'heading': heading, 'island_list': island_list, 'component_list': component_list, 'owner': owner}
	
	return render_to_response("templates/island_list.html", template_params, context_instance=(RequestContext(request)))


def item_history(request, slug, type, template_name='history.html'):

	if request.method == 'GET':
		
		try:
			class_type = globals()[type]
		except KeyError:
			return HttpResponseRedirect('/dponiwiki/')

		item = get_object_or_404(class_type, slug=slug)
		changes = item.changeset_set.all().order_by('-revision')

		# not sure if template_params is better than locals(), as above.
		# should probably choose one or the other, anyway.
		
		template_params = {'item': item,
                           'changes': changes}

		return render_to_response('templates/history.html',
                                  template_params, context_instance=(RequestContext(request)))

	return HttpResponseNotAllowed(['GET'])

def homepage_show(request):
	return render_to_response('templates/home.html', context_instance=(RequestContext(request)))

def revert_to_revision(request, slug, type):

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

	return HttpResponseNotAllowed(['POST'])


def view_changeset(request, type, slug, revision,
                   template_name='changeset.html',
                   *args, **kw):

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
                           'slug': slug}
		
		return render_to_response('templates/changeset.html',
                                  template_params,
                                  context_instance=RequestContext(request))
	return HttpResponseNotAllowed(['GET'])
    
    
def register(request):
	form = UserCreationFormExtended()
	
	if request.method == 'POST':
		form = UserCreationFormExtended(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect(reverse('login', kwargs={'next': '/islands/'}))
		else: form = UserCreationFormExtended()
		
	return render_to_response('templates/registration/registration_form.html', { 'form' : form }, context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('homepage'))