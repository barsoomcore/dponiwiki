import operator
from django.shortcuts import render_to_response, redirect
from django.views.generic.list_detail import object_detail
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from forms import IslandForm
from models import Island, IslandComponent, ComponentOrder

def display_island(request, slug, *args, **kwargs):
	# this wrapper gets the ordered list of components for the island and passes it 
	# to the template
	
	island = Island.objects.filter(slug__exact=slug)[0]
	if island.components:
		components = island.components.all()
		ordered_components = []
		for component in components:
			order = ComponentOrder.objects.filter(island__exact=island, component__exact=component)[0]
			setattr(component, 'order', order.order)
			ordered_components.append(component)
		ordered_components.sort(key=operator.attrgetter('order'))
		
		reorder_list = {}
		if len(ordered_components) > 1:
			for component in ordered_components:
				reorder_list[component.order] = component.name
		
	extra_context={'components': ordered_components, 'reorder_list': reorder_list}
	queryset = Island.objects.all()
	
	return object_detail(request, 
						queryset, 
						template_name='templates/island_detail.html', 
						template_object_name='island', 
						extra_context=extra_context,
						slug=slug
						)

@login_required
def update_island(request, slug=None):
	try:
		island = Island.objects.get(slug__exact=slug)
	except Island.DoesNotExist:
		island = None
	if request.method == 'POST':
		form = IslandForm(request.POST, instance=island)
		if form.is_valid():
			island = form.save(commit=False)
			if slug == None:
				island.owner = request.user
			island.save(editor=request.user)
			
			return HttpResponseRedirect(island.get_absolute_url())
	
	else:
		form = IslandForm(instance=island)
	
	return render_to_response('templates/island_form.html', locals(), context_instance=RequestContext(request))