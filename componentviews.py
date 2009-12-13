from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import ModelFormMetaclass, ModelForm
from django.template import RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.utils.translation import ugettext
from django.contrib.auth.views import redirect_to_login
from django.views.generic.create_update import get_model_and_form_class, apply_extra_context, redirect
from django import forms

from dponisetting.dponiwiki.models import Island, IslandComponent

# This bad boy was adapted from django.views.generic.create_update
# Needed to update the host island for the component as it saved
# Obviously we need to create a WRAPPER rather than copy-paste the whole function

def create_component(request, slug, model=None, template_name=None,
        template_loader=loader, extra_context=None, post_save_redirect=None,
        login_required=False, context_processors=None, form_class=None):
        
	if extra_context is None: extra_context = {}
	if login_required and not request.user.is_authenticated():
		return redirect_to_login(request.path)
	
	model, form_class = get_model_and_form_class(model, form_class)
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)
		if form.is_valid():
			new_object = form.save()
			post_save_redirect = "/dponiwiki/island/" + slug
			if request.user.is_authenticated():
				request.user.message_set.create(message=ugettext("The %(verbose_name)s was created successfully.") % {"verbose_name": model._meta.verbose_name})
			host_island = Island.objects.get(slug__exact=slug)
			if host_island:
				host_island.components.add(new_object)
			return redirect(post_save_redirect, new_object)
	else:
		form = form_class()

    # Create the template, context, response
	if not template_name:
		template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
	t = template_loader.get_template(template_name)
	c = RequestContext(request, {
		'form': form,
	}, context_processors)
	apply_extra_context(extra_context, c)
	return HttpResponse(t.render(c))

# likewise, here, create a wrapper instead of repeating the function.

def update_component(request, islandslug, componentslug, form_class):
	component = IslandComponent.objects.get(slug__exact=componentslug)
	if request.method == "POST":
		form = form_class(request.POST, request.FILES, instance=component)
		if form.is_valid():
			component = form.save()
#			if request.user.is_authenticated():
#				request.user.message_set.create(message=ugettext("The %(verbose_name)s was updated successfully.") % {"verbose_name": model._meta.verbose_name})
			post_save_redirect = "/dponiwiki/island/" + islandslug
			return redirect(post_save_redirect, component)
	else:
		form = form_class(instance=component)

	template_name = "dponiwiki/islandcomponent_form.html"
	template_loader = loader
	t = template_loader.get_template(template_name)
	c = RequestContext(request, {
		'form': form,
	})
	response = HttpResponse(t.render(c))
	return response

	
def assign_component(request, slug):
	component = IslandComponent.objects.get(slug__exact=slug)
	islands_list = Island.objects.exclude(components__id__exact=component.id)
	if request.method == "POST":
		for new_island in request.POST.values():
			new_island = Island.objects.get(slug__exact=new_island)
			component.host_islands.add(new_island)
		
	host_islands_list = component.host_islands.all()
	
	return render_to_response("dponiwiki/islandcomponent_assign.html", locals())