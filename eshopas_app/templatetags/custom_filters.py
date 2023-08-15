from django import template
from PIL import Image
import io

register = template.Library()

@register.filter
def resize_image(image, size):
    width, height = [int(x) for x in size.split('x')]

    img = Image.open(image)
    img.thumbnail((width, height), Image.ANTIALIAS)

    # Save the resized image to a BytesIO object
    image_io = io.BytesIO()
    img.save(image_io, format='JPEG')

    return image_io.getvalue()
