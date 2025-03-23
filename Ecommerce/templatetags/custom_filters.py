from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retrieve a dictionary item by key in Django templates."""
    return dictionary.get(key, [])
