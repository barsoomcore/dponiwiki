import re
from django import template
from django.db.models import Q
from django.template.defaultfilters import slugify
import textile

from dponisetting.dponiwiki.models import Island, IslandComponent

register = template.Library()

def custom_link(match):
	'''This is called in dinostyle and finds Islands or Components
	that match the term passed in. It tries to handle possessives
	and plurals, too.'''
	slug = slugify(match.group('name'))
	short_slug = slug[:-1]
	try:
		item = Island.objects.get(slug__iexact=slug)
	except Island.DoesNotExist:
		try:
			item = Island.objects.get(slug__iexact=short_slug)
		except Island.DoesNotExist:
			try:
				item = IslandComponent.objects.get(slug__iexact=slug)
			except IslandComponent.DoesNotExist:
				try:
					item = IslandComponent.objects.get(slug__iexact=short_slug)
				except IslandComponent.DoesNotExist:
					return match.group()
	
	return "\"" + match.group('name') + "\":" + item.get_absolute_url()


@register.filter
def dinostyle(content):
	
	# This regex goes for [[<name>]]
	pattern = re.compile(r'\[\[(?P<name>[^\]\]]*)\]\]')
	linked_content = pattern.sub(custom_link, content)
	
	return textile.textile(linked_content)