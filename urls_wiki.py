from django.conf.urls.defaults import *
import datetime
from tagging.views import tagged_object_list
from dponisetting.dponiwiki.models import Island, IslandComponent, StaticPage
from dponiwiki.forms import IslandForm, IslandComponentForm
from dponiwiki.feeds import LatestEntries, IslandFeed, IslandComponentFeed

island_dict = { 
	'queryset': Island.objects.all(),
	'template_name': 'templates/island_detail.html',
	'template_object_name': 'island' 
}

island_component_dict = {
	'queryset': IslandComponent.objects.all(),
	'template_name': 'templates/islandcomponent_detail.html',
	'template_object_name': 'component',
}

feeds = {
	'latest': LatestEntries,
	'Island': IslandFeed,
	'IslandComponent': IslandComponentFeed,
}

urlpatterns = patterns('',
    url(r'^$', 
    	'django.views.generic.simple.redirect_to', 
    	{'url': '/dponiwiki/page/home/' }, 
    	name="homepage"
    ),
    url(r'^markup/$', 
    	'django.views.generic.simple.direct_to_template', 
    	{'template': 'markup.html'}, 
    	name='markup'
    ),
    url(r'^accounts/', include('dponisetting.dponiwiki.urls_registration')),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    url(r'^page/', include('dponisetting.dponiwiki.urls_static')),
	url(r'^Island/(?P<slug>[-\w]+)/$', 
		'django.views.generic.list_detail.object_detail', 
		island_dict, 
		name='island-detail'
	),
	url(r'^IslandComponent/(?P<slug>[-\w]+)/$',
		'django.views.generic.list_detail.object_detail',
		island_component_dict,
		name='component-detail'
	),
)

urlpatterns += patterns('dponisetting.dponiwiki.utilityviews',
	url(r'^canonical/(?P<canonicity>[-\w]+)/$',	'canonical', name='island-canonical'),
	url(r'^search/(?P<type>[-\w]+)/$', 'search', name='search'),
	url(r'^owner/$', 'by_owner', name='owner-search'),
	url(r'^owner/(?P<owner>[-\w]+)/$', 'by_owner', name='owner'),
    url(r'^(?P<type>[-\w]+)/history/(?P<slug>[-\w]+)/$', 'item_history', name='item_history'),
    url(r'^accounts/register/$', 'register', name="register"),
	url(r'^history/(?P<slug>[-\w]+)/(?P<type>[-\w]+)/revert/$', 
		'revert_to_revision', 
		name='wiki_revert_to_revision'
	),
	url(r'^history/(?P<slug>[-\w]+)/(?P<type>[-\w]+)/changeset/(?P<revision>[-\w]+)/$', 
		'view_changeset', 
		name='wiki_changeset'
	),
	url(r'^components/tag/(?P<url>.*)/$', 'by_tags', name='component_tag_detail'),
)

urlpatterns += patterns('dponisetting.dponiwiki.componentviews',
	url(r'^create-component/$', 'update_component', name='create-component',),
	url(r'^Island/(?P<islandslug>[-\w]+)/create-component/$', 
		'update_component', 
		name='create-component-island', 
	),
	url(r'^Island/(?P<islandslug>[-\w]+)/update-component/(?P<componentslug>[-\w]+)/$', 
		'update_component', 
		name='update-component', 
	),
	url(r'^assign-component/(?P<slug>[-\w]+)/$', 'assign_component', name='assign-component', ),
	url(r'^Island/(?P<islandslug>[-\w]+)/move-component/(?P<componentslug>[-\w]+)/$', 
		'move_component', 
		name='move_component', 
	),
	url(r'^Island/(?P<islandslug>[-\w]+)/remove-component/(?P<componentslug>[-\w]+)/$', 
		'remove_component', 
		name='remove_component', 
	),
)

urlpatterns += patterns('dponisetting.dponiwiki.islandviews',
	url(r'^create-island/$', 'update_island', name='create-island'),
	url(r'^update-island/(?P<slug>[-\w]+)/$', 'update_island', name='update-island' ),
)