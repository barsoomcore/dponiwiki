from django.shortcuts import render_to_response, redirect
from django.views.generic.create_update import create_object, update_object

from dponisetting.dponiwiki.models import Island, IslandComponent, ComponentOrder


def create_component_wrapper(request, slug, *args, **kwargs):
	# this little trick lets us assign the newly created component to its host island
	assign_url = "/dponiwiki/assign-new-component/" + slug
	return create_object(request, post_save_redirect = assign_url + "/%(slug)s", *args, **kwargs)


def assign_new_component(request, islandslug, componentslug):
	# called in create_component_wrapper to finish the job of assigning the new component
	island = Island.objects.get(slug__exact=islandslug)
	new_component = IslandComponent.objects.get(slug__exact=componentslug)
	new_order_order = 1 #there could be a better name for this.
	if island:
		current_order = ComponentOrder.objects.filter(island__exact=island).order_by('order')
		if current_order:
			for item in current_order:
				if item.order == new_order_order:
					new_order_order = new_order_order + 1
					
		new_order = ComponentOrder(island=island, component=new_component, order=new_order_order)
		new_order.save()
		island.save(latest_comment="Added Component " + new_component.name)
		
	return redirect("/dponiwiki/Island/" + islandslug)


def update_component_wrapper(request, islandslug, componentslug, *args, ** kwargs):
	return update_object(request, slug=componentslug, 
		post_save_redirect='/dponiwiki/Island/' + islandslug, *args, **kwargs)

	
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
			new_island.save(latest_comment="Added Component " + component.name)
		
	host_islands_list = component.host_islands.all()
	
	return render_to_response("dponiwiki/islandcomponent_assign.html", locals())