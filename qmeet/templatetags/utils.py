from django import template
register = template.Library()


@register.filter(name='iterations')
def interations(times_to_loop):
    return range(times_to_loop)


@register.filter(name='to_int')
def to_int(string_to_cast):
    return int(string_to_cast)


@register.filter(name='index')
def index(position, i):
    return position[i]
