from django import template

register = template.Library()

@register.filter
def isabsent(item, list1):
	if item not in list1:
		return True
	else:
		return False