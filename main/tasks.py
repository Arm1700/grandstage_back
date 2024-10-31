from celery import shared_task
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

@shared_task
def optimize_image(image_id):
    from .models import Gallery
    try:
        gallery = Gallery.objects.get(id=image_id)
        if gallery.img:
            img = Image.open(gallery.img)
            output = BytesIO()

            img = img.convert('RGB')
            img.thumbnail((800, 800), Image.ANTIALIAS)
            img.save(output, format='JPEG', quality=60)
            output.seek(0)

            gallery.img = InMemoryUploadedFile(output, 'ImageField', f"{gallery.img.name.split('.')[0]}.jpg", 'image/jpeg', sys.getsizeof(output), None)
            gallery.save()
    except Gallery.DoesNotExist:
        pass
