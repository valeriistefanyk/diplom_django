from django.template import Library

register = Library()

@register.simple_tag
def update_variable(value):
    return value