from django import template
from imagekit.processors import ResizeToFill

register = template.Library()

class ResizeImageProcessor(ResizeToFill):
    width = 150
    height = 200
    upscale = False

@register.filter
def resize_image(image_url):
    processor = ResizeImageProcessor()
    return processor.process(image_url)
