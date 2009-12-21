from django.conf.urls.defaults import *
from django.contrib.auth.views import login
from dponisetting.dponiwiki.models import Island, IslandComponent
from dponiwiki.forms import IslandForm, IslandComponentForm

island_dict = { 'queryset': Island.objects.all(), 'template_object_name': 'island' }
component_dict = { 'queryset': IslandComponent.objects.all(), 'template_object_name': 'component' }
island_form_dict = { 'form_class': IslandForm }
component_form_dict = { 'form_class': IslandComponentForm }

urlpatterns = patterns('',
    url(r'^accounts/login/$',  login, {'template_name': 'registration/login.html'}, name='login'),
)

urlpatterns += patterns('dponisetting.dponiwiki.utilityviews',
	url(r'^canonical/(?P<canonicity>[-\w]+)/$', 'canonical', name='island-canonical'),
	url(r'^search/(?P<type>[-\w]+)/$', 'search', name='search'),
	url(r'^user/$', 'by_user', name='island-user'),
    url(r'^(?P<type>[-\w]+)/history/(?P<slug>[-\w]+)/$', 'item_history', name='item_history'),
    url(r'^accounts/register/$', 'register', name="register"),
	url(r'^history/(?P<slug>[-\w]+)/(?P<type>[-\w]+)/revert/$', 'revert_to_revision', name='wiki_revert_to_revision'),
	url(r'^history/(?P<slug>[-\w]+)/(?P<type>[-\w]+)/changeset/(?P<revision>[-\w]+)/$', 'view_changeset', name='wiki_changeset'),
    url(r'^accounts/logout/$', 'logout_view', name='logout'),
)

urlpatterns += patterns('dponisetting.dponiwiki.componentviews',
	url(r'^Island/(?P<slug>[-\w]+)/create-component/$', 'create_component_wrapper', component_form_dict, name='public-component-create', ),
	url(r'^Island/(?P<islandslug>[-\w]+)/update-component/(?P<componentslug>[-\w]+)/$', 'update_component_wrapper', component_form_dict, name='public-component-update', ),
	url(r'^assign-component/(?P<slug>[-\w]+)/$', 'assign_component', name='component-assign', ),
	url(r'^assign-new-component/(?P<islandslug>[-\w]+)/(?P<componentslug>[-\w]+)/$', 'assign_new_component', name='assign-new-component', ),
)

urlpatterns += patterns('django.views.generic.create_update',
	url(r'^create-island/$', 'create_object', island_form_dict, name='public-create'),
	url(r'^update-island/(?P<slug>[-\w]+)/$', 'update_object', island_form_dict, name='public-island-update' ),
)

urlpatterns += patterns('django.views.generic.list_detail',
	url(r'^Island/(?P<slug>[-\w]+)/$', 'object_detail', island_dict, name='island-detail'),
	url(r'^IslandComponent/(?P<slug>[-\w]+)/$', 'object_detail', component_dict, name='component-detail'), 
	url(r'^islands/$', 'object_list', island_dict, name='island-list'),
	url(r'^components/$', 'object_list', component_dict, name='component-list'),
)