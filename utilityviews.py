from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext

from dponisetting.dponiwiki.models import Island, IslandComponent, ChangeSet

def canonical(request, canonicity):
	island_list = Island.objects.filter(iscanonical=canonicity)
	if canonicity == "True":
		heading = "Canonical Islands"
	else:
		heading = "Non-Canonical Islands"
	return render_to_response("dponiwiki/island_list.html", locals())

	
def search(request, component_type):
	if 'q' in request.GET:
		term = request.GET['q']
		
		# really think there ought to be a way of simply casting component_type to
		#    be interpreted as the class directly, instead of this if statement.
		if component_type == "Island":
			island_list = Island.objects.filter(Q(name__contains=term) | Q(summary__contains=term))
		elif component_type == "Component":
			island_list = IslandComponent.objects.filter(Q(name__contains=term) | Q(content__contains=term))
		
		heading = "Search Results: All " +component_type + "s containing the term \"" + term + "\""
			
	return render_to_response("dponiwiki/island_list.html", locals())


def by_user(request):
	if 'q' in request.GET:
		owner = request.GET['q']
		
		# good enough for Islands but what about IslandComponents?
		
		island_list = Island.objects.filter(owner__username__iexact=owner)
		heading = "All Islands Owned By \"" + owner + "\""
	
	return render_to_response("dponiwiki/island_list.html", locals())


def item_history(request, slug, type, template_name='history.html'):

    if request.method == 'GET':
    
    	# again, having no real idea how to get directly from type to a class name
    	# this is a different solution, but surely there's something better
    	
    	types = dict({'island': 'Island', 'component': 'IslandComponent'})
    	class_type = globals()[types[type]]

        item = get_object_or_404(class_type, slug=slug)
        changes = item.changeset_set.all().order_by('-revision')

		# not sure if template_params is better than locals(), as above.
		# should probably choose one or the other, anyway.
		
        template_params = {'item': item,
                           'changes': changes}

        return render_to_response('dponiwiki/history.html',
                                  template_params)

    return HttpResponseNotAllowed(['GET'])


def revert_to_revision(request, slug, type):

    if request.method == 'POST':
    
    	# okay, now that I'm doing this twice I should pull it out and
    	#    make it into a function I guess. Still think there must be a
    	# simpler solution
    	
    	types = dict({'island': 'Island', 'component': 'IslandComponent'})
    	class_type = globals()[types[type]]

        item = get_object_or_404(class_type, slug=slug)

        revision = int(request.POST['revision'])

        item.revert_to(revision)
        
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
    	# also, get rid of the "article" terminology left over from wiki-app
    	
        article_args = {'component__slug': slug}

        changeset = get_object_or_404(
            ChangeSet.objects.all().select_related(),
            revision=int(revision),
            **article_args)

        article = changeset.component

        template_params = {'article': article,
                           'article_name': article.name,
                           'changeset': changeset,
                           'slug': slug}

		# don't know what the RequestContext() is doing here
		
        return render_to_response('dponiwiki/changeset.html',
                                  template_params,
                                  context_instance=RequestContext(request))
    return HttpResponseNotAllowed(['GET'])
    
    
def register(request):
	form = UserCreationForm()
	
	if request.method == 'POST':
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect('/dponiwiki/')
		else: form = UserCreationForm()
		
	return render_to_response('registration/register.html', { 'form' : form })