from django import template
import json


register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def multiply(value, arg):
    return value * arg
