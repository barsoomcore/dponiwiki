from django.conf.urls.defaults import *
from django.contrib.auth.views import login
import datetime
from tagging.views import tagged_object_list
from dponisetting.dponiwiki.models import Island, IslandComponent, StaticPage
from dponiwiki.forms import IslandForm, IslandComponentForm

island_dict = { 
	'queryset': Island.objects.all(), 
	'template_object_name': 'island' 
}
island_list_dict = { 
	'queryset': Island.objects.all(), 
	'template_name': 'templates/island_list.html', 
	'template_object_name': 'island' 
}
island_canonical_list_dict = { 
	'queryset': Island.objects.filter(iscanonical=True), 
	'template_name': 'templates/island_list.html', 
	'template_object_name': 'island' 
}
component_dict = { 
	'queryset': IslandComponent.objects.all(), 
	'template_name': 'templates/islandcomponent_detail.html', 
	'template_object_name': 'component'
}
component_list_dict = { 
	'queryset': IslandComponent.objects.all(),
	'template_name': 'templates/islandcomponent_list.html', 
	'template_object_name': 'component' 
}
component_tag_dict = {
	'queryset_or_model': IslandComponent, 
	'paginate_by': 25,
	'template_name':'templates/islandcomponent_list.html',
	'allow_empty':True, 
	'template_object_name':'component'
}

last_week = datetime.datetime.now() - datetime.timedelta(days=7)
latest_updates = Island.objects.filter(modified__gte=last_week).filter(iscanonical=True)[:10]
extra_context = {'latest_updates': latest_updates }
page_dict = {
	'queryset': StaticPage.objects.all(),
	'template_name': 'templates/page_detail.html',
	'template_object_name': 'page',
	'extra_context': extra_context
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/dponiwiki/page/home/' }, name="homepage"),
    url(r'^components/tag/(?P<tag>[^/]+)/$', tagged_object_list, component_tag_dict, name='component_tag_detail'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^accounts/login/$',  login, {'template_name': 'templates/registration/login.html'}, name='login'),
    url(r'^accounts/logout/$', 'logout', {'next_page': '/dponiwiki/'}, name='logout'),
	url(r'^accounts/password_change/$', 'password_change', {'template_name': 'templates/registration/password_change_form.html'}, name='password_reset'),
	url(r'^accounts/password_change/done/$', 'password_change_done', {'template_name': 'templates/registration/password_change_done.html'}),
)


urlpatterns += patterns('dponisetting.dponiwiki.utilityviews',
	url(r'^canonical/(?P<canonicity>[-\w]+)/$', 'canonical', name='island-canonical'),
	url(r'^search/(?P<type>[-\w]+)/$', 'search', name='search'),
	url(r'^user/$', 'by_user', name='user-search'),
	url(r'^user/(?P<user>[-\w]+)/$', 'by_user', name='user'),
    url(r'^(?P<type>[-\w]+)/history/(?P<slug>[-\w]+)/$', 'item_history', name='item_history'),
    url(r'^accounts/register/$', 'register', name="register"),
	url(r'^history/(?P<slug>[-\w]+)/(?P<type>[-\w]+)/revert/$', 'revert_to_revision', name='wiki_revert_to_revision'),
	url(r'^history/(?P<slug>[-\w]+)/(?P<type>[-\w]+)/changeset/(?P<revision>[-\w]+)/$', 'view_changeset', name='wiki_changeset'),
)

urlpatterns += patterns('dponisetting.dponiwiki.componentviews',
	url(r'^IslandComponent/(?P<slug>[-\w]+)/$', 'display_component', name='component-detail'), 
	url(r'^Island/(?P<islandslug>[-\w]+)/create-component/$', 'update_component', name='public-component-create', ),
	url(r'^Island/(?P<islandslug>[-\w]+)/update-component/(?P<componentslug>[-\w]+)/$', 'update_component', name='public-component-update', ),
	url(r'^assign-component/(?P<slug>[-\w]+)/$', 'assign_component', name='component-assign', ),
	url(r'^Island/(?P<islandslug>[-\w]+)/move-component/(?P<componentslug>[-\w]+)/$', 'move_component', name='move_component', ),
	url(r'^Island/(?P<islandslug>[-\w]+)/remove-component/(?P<componentslug>[-\w]+)/$', 'remove_component', name='remove_component', ),
)

urlpatterns += patterns('dponisetting.dponiwiki.islandviews',
	url(r'^Island/(?P<slug>[-\w]+)/$', 'display_island', island_dict, name='island-detail'),
	url(r'^create-island/$', 'update_island', name='public-create'),
	url(r'^update-island/(?P<slug>[-\w]+)/$', 'update_island', name='public-island-update' ),
)

urlpatterns += patterns('django.views.generic.list_detail',
	url(r'^islands/$', 'object_list', island_canonical_list_dict, name='island-list'),
	url(r'^components/$', 'object_list', component_list_dict, name='component-list'),
    url(r'^page/(?P<slug>[-\w]+)/$', 'object_detail', page_dict, name='page-detail'),
)