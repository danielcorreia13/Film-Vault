from django import template
register = template.Library()

@register.filter
def isList(l):
    return isinstance(l, list)