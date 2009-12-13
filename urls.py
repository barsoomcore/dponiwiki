from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from dponisetting.dponiwiki.models import Island, IslandComponent
from dponiwiki.forms import IslandForm, IslandComponentForm

island_dict = { 'queryset': Island.objects.all(), 'template_object_name': 'island' }
component_dict = { 'queryset': IslandComponent.objects.all(), 'template_object_name': 'component' }
island_form_dict = { 'form_class': IslandForm }
component_form_dict = { 'form_class': IslandComponentForm }

urlpatterns = patterns('',
    url(r'^accounts/login/$',  login, {'template_name': 'registration/login.html'}),
    url(r'^accounts/logout/$', logout),
)

urlpatterns += patterns('dponisetting.dponiwiki.utilityviews',
	url(r'^canonical/(?P<canonicity>[-\w]+)/$', 'canonical', name='island-canonical'),
	url(r'^search/(?P<component_type>[-\w]+)/$', 'search', name='search'),
	url(r'^user/$', 'by_user', name='island-user'),
    url(r'^(?P<type>[-\w]+)/history/(?P<slug>[-\w]+)/$', 'item_history', name='item_history'),
    url(r'^accounts/register/$', 'register', name="register"),
	url(r'^history/(?P<slug>[-\w]+)/(?P<type>[-\w]+)/revert/$', 'revert_to_revision', name='wiki_revert_to_revision'),
	url(r'^history/(?P<slug>[-\w]+)/(?P<type>[-\w]+)/changeset/(?P<revision>[-\w]+)/$', 'view_changeset', name='wiki_changeset'),
)

urlpatterns += patterns('dponisetting.dponiwiki.componentviews',
	url(r'^island/(?P<slug>[-\w]+)/create-component/$', 'create_component', component_form_dict, name='public-component-create', ),
	url(r'^island/(?P<islandslug>[-\w]+)/update-component/(?P<componentslug>[-\w]+)/$', 'update_component', component_form_dict, name='public-component-update', ),
	url(r'^assign-component/(?P<slug>[-\w]+)/$', 'assign_component', name='component-assign', ),
)

urlpatterns += patterns('django.views.generic.create_update',
	url(r'^create-island/$', 'create_object', island_form_dict, name='public-create'),
	url(r'^update-island/(?P<slug>[-\w]+)/$', 'update_object', island_form_dict, name='public-island-update' ),
)

urlpatterns += patterns('django.views.generic.list_detail',
	url(r'^island/(?P<slug>[-\w]+)/$', 'object_detail', island_dict, name='island-detail'),
	url(r'^component/(?P<slug>[-\w]+)/$', 'object_detail', component_dict, name='component-detail'), 
	url(r'^islands/$', 'object_list', island_dict, name='island-list'),
	url(r'^components/$', 'object_list', component_dict, name='component-list'),
)