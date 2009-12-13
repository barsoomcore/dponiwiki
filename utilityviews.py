from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

from dponisetting.dponiwiki.models import Island, IslandComponent

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
		if component_type == "Island":
			island_list = Island.objects.filter(Q(name__contains=term) | Q(summary__contains=term))
			heading = "Search Results: All Islands Containing \"" + term + "\""
		elif component_type == "Component":
			island_list = IslandComponent.objects.filter(Q(name__contains=term) | Q(content__contains=term))
			heading = "Search Results: All Components Containing \"" + term + "\""
			
	return render_to_response("dponiwiki/island_list.html", locals())


def by_user(request):
	if 'q' in request.GET:
		owner = request.GET['q']
		island_list = Island.objects.filter(owner__username__iexact=owner)
		heading = "All Islands Owned By \"" + owner + "\""
	
	return render_to_response("dponiwiki/island_list.html", locals())


def item_history(request, slug, type, template_name='history.html'):

    if request.method == 'GET':
    	types = dict({'island': 'Island', 'component': 'IslandComponent'})
    	class_type = globals()[types[type]]

        item = get_object_or_404(class_type, slug=slug)
        changes = item.changeset_set.all().order_by('-revision')

        template_params = {'item': item,
                           'changes': changes}

        return render_to_response('dponiwiki/history.html',
                                  template_params)

    return HttpResponseNotAllowed(['GET'])


def revert_to_revision(request, slug, type):

    if request.method == 'POST':
    	types = dict({'island': 'Island', 'component': 'IslandComponent'})
    	class_type = globals()[types[type]]

        item = get_object_or_404(class_type, slug=slug)

        revision = int(request.POST['revision'])

        item.revert_to(revision)
                
        url = '/dponiwiki/' + type + '/history/' + slug
        
        return HttpResponseRedirect(url)

    return HttpResponseNotAllowed(['POST'])
    
    
def register(request):
	form = UserCreationForm()
	
	if request.method == 'POST':
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect('/dponiwiki/')
		else: form = UserCreationForm()
		
	return render_to_response('registration/register.html', { 'form' : form })