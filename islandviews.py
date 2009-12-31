import operator
from django.shortcuts import render_to_response, redirect
from django.views.generic.list_detail import object_detail

from dponisetting.dponiwiki.models import Island, IslandComponent, ComponentOrder

def display_island(request, slug, *args, **kwargs):
	island = Island.objects.filter(slug__exact=slug)[0]
	if island.components:
		components = island.components.all()
		ordered_components = []
		for component in components:
			order = ComponentOrder.objects.filter(island__exact=island, component__exact=component)[0]
			setattr(component, 'order', order.order)
			ordered_components.append(component)
		ordered_components.sort(key=operator.attrgetter('order'))
	extra_context={'components': ordered_components}
	queryset = Island.objects.all()
	
	return object_detail(request, queryset, template_object_name='island', extra_context=extra_context, slug=slug)