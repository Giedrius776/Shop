from django import template
from PIL import Image
import os


register = template.Library()

@register.filter
def resize_image(image_path, size):
    print("Image Path:", image_path)  # Add this line for debugging
    try:
        img = Image.open(image_path)
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(image_path)
        return image_path
    except Exception as e:
        return str(e)


register = template.Library()

@register.filter
def get_by_id(list_items, item_id):
    try:
        return next(item for item in list_items if item.id == item_id)
    except StopIteration:
        return None