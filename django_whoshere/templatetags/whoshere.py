from django import template

from django_whoshere.apps import get_ip, parse, get_city, get_country
from django_whoshere.models import UserSession

register = template.Library()


@register.simple_tag(name='active_user_count')
def user_count():
    return UserSession.active_user_count()


@register.assignment_tag(name='active_users')
def active_users():
    return UserSession.active_users()


@register.simple_tag(name='your_ip', takes_context=True)
def user_ip(context):
    return get_ip(context['request'])


@register.simple_tag(name='your_agent', takes_context=True)
def user_agent(context):
    agent = context['request'].META.get('HTTP_USER_AGENT', '')
    if parse:
        return parse(agent)
    return agent


@register.simple_tag(name='your_city', takes_context=True)
def user_city(context):
    ip = get_ip(context['request'])
    return get_city(ip)


@register.simple_tag(name='your_country', takes_context=True)
def user_country(context):
    ip = get_ip(context['request'])
    return get_country(ip)
