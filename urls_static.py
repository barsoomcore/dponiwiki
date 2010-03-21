from django.conf.urls.defaults import *
import datetime
from dponisetting.dponiwiki.models import Island, StaticPage

latest_updates = ''
last_week = datetime.datetime.now() - datetime.timedelta(days=7)
latest_updates = Island.objects.filter(modified__gte=last_week).filter(iscanonical=True)[:10]
latest_context = {'latest_updates': latest_updates }
page_dict = {
	'queryset': StaticPage.objects.all(),
	'template_name': 'templates/page_detail.html',
	'template_object_name': 'page',
	'extra_context': latest_context
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^(?P<slug>[-\w]+)/$', 'object_detail', page_dict, name='page-detail'),
)