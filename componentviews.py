from django.shortcuts import render_to_response, redirect
from django.views.generic.create_update import create_object, update_object
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from forms import IslandComponentForm
from models import Island, IslandComponent, ComponentOrder

@login_required
def assign_component(request, slug):
	component = IslandComponent.objects.get(slug__exact=slug)
	islands_list = Island.objects.exclude(components__id__exact=component.id)
	if request.method == "POST":
		for new_island in request.POST.values():
			new_island = Island.objects.get(slug__exact=new_island)
			current_order = ComponentOrder.objects.filter(island__exact=new_island).order_by('order')
			new_order_order = 1
			if current_order:
				for item in current_order:
					if item.order == new_order_order:
						new_order_order = new_order_order + 1
					
			new_order = ComponentOrder(island=new_island, component=component, order=new_order_order)
			new_order.save()
			new_island.save(latest_comment="Added Component " + component.name, editor=request.user)
		
	host_islands_list = component.host_islands.all()
	
	return render_to_response("dponiwiki/islandcomponent_assign.html", locals())

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
					current_order = ComponentOrder.objects.filter(island__exact=island).order_by('order')
					new_order_order = 1
					if current_order:
						for item in current_order:
							if item.order == new_order_order:
								new_order_order = new_order_order + 1
					
					new_order = ComponentOrder(island=island, component=component, order=new_order_order)
					new_order.save()
					island.save(latest_comment="Added Component " + component.name, editor=request.user)
				
				else:
					island.save(latest_comment="Updated Component " + component.name, editor=request.user)
				
				return HttpResponseRedirect(island.get_absolute_url())
			
			else:
				return HttpResponseRedirect(component.get_absolute_url())
	
	else:
		form = IslandComponentForm(instance=component)
	
	return render_to_response('dponiwiki/islandcomponent_form.html', {'form': form}, context_instance=RequestContext(request))