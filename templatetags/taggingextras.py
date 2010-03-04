from django import template

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