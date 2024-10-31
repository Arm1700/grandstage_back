from adminsortable.models import SortableMixin
from django.core.exceptions import ValidationError
from django.db import models
import json


class Event(models.Model):
    day = models.PositiveIntegerField()
    month = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    hour = models.CharField(max_length=50)
    place = models.CharField(max_length=100)
    event_description = models.TextField()
    description = models.TextField()
    image = models.URLField(max_length=200)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('expired', 'Expired')
    ])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Outcome(models.Model):
    event = models.ForeignKey(Event, related_name='outcomes', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='course_photos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)
    desc = models.TextField(default='', blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Ensure the base save is called
        images = form.cleaned_data.get('img', [])
        for image in images:
            Gallery.objects.create(course=obj, img=image)


class Gallery(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='gallery_photos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Gallery {self.id} - {self.course.name}" if self.course else "Gallery"


class Certificate(models.Model):
    img = models.ImageField(upload_to='certificate_photos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Certificate {self.id} "

