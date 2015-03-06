__author__ = 'Daniel'
from django import template
from django.db.models import Q
import datetime
from django.utils import timezone

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

@register.filter
def get_alarm_type(value):
    if datetime.date.today() >= value.outboundDate - datetime.timedelta(days=1):
        return 1
    elif datetime.date.today() >= value.outboundDate - datetime.timedelta(days=4) and datetime.date.today() < value.outboundDate - datetime.timedelta(days=1):
        return 2
    else:
        return 3

@register.filter
def validate_work(value):
    now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    if now <= value.limitResponseDate:
        return True
    else:
        return False