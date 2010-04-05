import re
from django import template
from markup import textile

from dponisetting.dponiwiki.models import Island, IslandComponent

register = template.Library()

@register.filter
def isabsent(item, list1):
	if item not in list1:
		return True
	else:
		return False

@register.filter
def matches(list1, list2):
	if set(list1) == set(list2):
		return True
	else:
		return False

def custom_link(match):
	try:
		item = Island.objects.get(name__exact=match.group('name'))
	except Island.DoesNotExist:
		try:
			item = IslandComponent.objects.get(name__exact=match.group('name'))
		except IslandComponent.DoesNotExist:
			return match.group()
	
	return "\"" + match.group('name') + "\":" + item.get_absolute_url()


@register.filter
def dinostyle(content):
	pattern = re.compile(r'\[\[(?P<name>[^\]\]]*)\]\]')
	linked_content = pattern.sub(custom_link, content)
	
	return textile(linked_content)