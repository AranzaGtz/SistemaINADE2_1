from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})

@register.filter
def length_is(value, arg):
    """Returns True if the length of the value is equal to arg."""
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False