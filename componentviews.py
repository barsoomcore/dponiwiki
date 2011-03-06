from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import create_object, update_object
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from forms import IslandComponentForm
from models import Island, IslandComponent, ComponentOrder
from utilityviews import paginate

@login_required
def assign_component(request, slug):
	component = get_object_or_404(IslandComponent, slug__exact=slug)
	islands_list = Island.objects.filter(owner__exact=component.owner).exclude(components__id__exact=component.id)
	host_islands_list = component.host_islands.all()
	new_islands_list = []
	if request.method == "POST":
		for island in request.POST.values():
			new_island = Island.objects.get(slug__exact=island)
			if not new_island in host_islands_list:
				new_islands_list.append(new_island)
				component.add_component_to_end(request.user, new_island)
	
	host_islands_list = component.host_islands.all()[:10]
	
	islands = paginate(request, islands_list)
	
	template_params = {
		'component': component, 
		'islands_list': islands, 
		'host_islands_list': host_islands_list,
		'new_islands_list': new_islands_list
	}
	
	return render_to_response(
		"templates/islandcomponent_assign.html", 
		template_params, 
		context_instance=RequestContext(request)
	)

@login_required
def update_component(request, islandslug=None, componentslug=None):
	try:
		island = Island.objects.get(slug__exact=islandslug)
	except Island.DoesNotExist:
		island = None
	try:
		component = IslandComponent.objects.get(slug__exact=componentslug)
	except IslandComponent.DoesNotExist:
		component = None
	
	if request.method == 'POST':
		form = IslandComponentForm(request.POST, instance=component)
		if form.is_valid():
			component = form.save(commit=False)
			if componentslug == None:
				component.owner = request.user
			component.save(editor=request.user)
			
			if island:
				if component not in island.components.all():					
					component.add_component_to_end(request.user, island)
					
				return HttpResponseRedirect(island.get_absolute_url())
			
			else:
				return HttpResponseRedirect(component.get_absolute_url())
	
	else:
		form = IslandComponentForm(instance=component)
	
	return render_to_response(
		'templates/islandcomponent_form.html', 
		locals(), 
		context_instance=RequestContext(request)
	)

@login_required
def move_component(request, islandslug, componentslug):
	island = get_object_or_404(Island, slug__exact=islandslug)
	component = get_object_or_404(IslandComponent, slug__exact=componentslug)
	current_order = ComponentOrder.objects.filter(island__exact=island).order_by('order')
	
	if request.method == 'POST':
		new_component_position = int(request.POST.values()[0])
		for item in current_order:
			if item.component == component:
				item.order = new_component_position
				item.save()
			else:
				if item.order >= new_component_position:
					item.order = item.order + 1
					item.save()
		island.save(latest_comment="Moved Component " + component.name, editor=request.user)
	
	return HttpResponseRedirect(island.get_absolute_url())

@login_required
def remove_component(request, islandslug, componentslug):
	island = get_object_or_404(Island, slug__exact=islandslug)
	component = get_object_or_404(IslandComponent, slug__exact=componentslug)
	ComponentOrder.objects.filter(island__exact=island).filter(component__exact=component).delete()
	
	island.save(latest_comment="Removed Component " + component.name, editor=request.user)
	
	return HttpResponseRedirect(island.get_absolute_url())