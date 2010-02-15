from django.contrib.syndication.feeds import Feed
from dponisetting.dponiwiki.models import Island, IslandComponent

class LatestEntries(Feed):
	title = "DINO-PIRATES OF NINJA ISLAND"
	link = "/dponiwiki/"
	description = 'New Islands on DINO-PIRATES OF NINJA ISLAND'
	
	def items(self):
		return Island.objects.order_by('created')[:5]
	
	description_template = 'templates/feeds/latest_description.html'

class IslandFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Island.objects.get(slug__exact=bits[0])

    def title(self, obj):
        return "DINO-PIRATES OF NINJA ISLAND: Updates for Island %s" % obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return 'Updates to %s' % obj.name

    def items(self, obj):
       return obj.changeset_set.all().order_by('-revision')[:30]
       
    title_template = 'templates/feeds/island_title.html'
    description_template = 'templates/feeds/island_description.html'

class IslandComponentFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return IslandComponent.objects.get(slug__exact=bits[0])

    def title(self, obj):
        return "DINO-PIRATES OF NINJA ISLAND: Updates for Component %s" % obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return 'Updates to %s' % obj.name

    def items(self, obj):
       return obj.changeset_set.all().order_by('-revision')[:30]
       
    title_template = 'templates/feeds/island_title.html'
    description_template = 'templates/feeds/island_description.html'