from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import ModelFormMetaclass, ModelForm
from django.template import RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.utils.translation import ugettext
from django.contrib.auth.views import redirect_to_login
from django.views.generic.create_update import get_model_and_form_class, apply_extra_context, redirect, create_object, update_object
from django import forms

from dponisetting.dponiwiki.models import Island, IslandComponent


def create_component_wrapper(request, slug, *args, **kwargs):
	# this little trick lets us assign the newly created component to its host island
	assign_url = "/dponiwiki/assign-new-component/" + slug
	return create_object(request, post_save_redirect = assign_url + "/%(slug)s", *args, **kwargs)


def assign_new_component(request, islandslug, componentslug):
	# called in create_component_wrapper to finish the job of assigning the new component
	island = Island.objects.get(slug__exact=islandslug)
	new_component = IslandComponent.objects.get(slug__exact=componentslug)
	if island:
		island.components.add(new_component)
	
	return render_to_response("dponiwiki/island_detail.html", locals())


def update_component_wrapper(request, islandslug, componentslug, *args, ** kwargs):
	return update_object(request, slug=componentslug, post_save_redirect='/dponiwiki/Island/'+islandslug, *args, **kwargs)

	
def assign_component(request, slug):
	component = IslandComponent.objects.get(slug__exact=slug)
	islands_list = Island.objects.exclude(components__id__exact=component.id)
	if request.method == "POST":
		for new_island in request.POST.values():
			new_island = Island.objects.get(slug__exact=new_island)
			component.host_islands.add(new_island)
		
	host_islands_list = component.host_islands.all()
	
	return render_to_response("dponiwiki/islandcomponent_assign.html", locals())