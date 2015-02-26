__author__ = 'Daniel'
from django import template
from django.db.models import Q
register = template.Library()

@register.filter
def get_accepted(value, arg):
    value.filter()
    return value.filter(Q(accepted=arg) & Q(responseDate__isnull=False))

@register.filter
def get_no_response(value):
    return value.filter(responseDate=None)

@register.filter
def get_total_capacity(value):
    sum = 0;
    for aff in value:
        sum += aff.capacity
    return sum