from django import template

register = template.Library()

@register.filter
def removePage(value):
    return value.replace("page&","")