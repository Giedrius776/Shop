from django import template
from eshopas_app.models import Cart

register = template.Library()

@register.filter(name='cart_items_count', app='eshopas_app')
def cart_items_count(cart):
    # Your filter logic here
    pass
