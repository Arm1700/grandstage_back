from django.contrib import admin

from .forms import GalleryForm
from .models import Course, Gallery, Certificate
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


class GalleryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Gallery
    form = GalleryForm  # Use the form with MultiImageField
    extra = 1  # Number of empty rows for adding galleries


@admin.register(Course)
class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'order')
    ordering = ['order']
    inlines = [GalleryInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Ensure the base save is called
        images = form.cleaned_data.get('img', [])
        for image in images:
            Gallery.objects.create(course=obj, img=image)


@admin.register(Certificate)
class CertificateAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order')
    fields = ['img']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'order')
    fields = ['course', 'img']  # Убираем 'order'
