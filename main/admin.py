from django.contrib import admin
from .forms import GalleryForm
from .models import Course, Gallery, Certificate
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


class GalleryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Gallery
    extra = 0
    fields = ['img', 'order']
    sortable_field_name = "order"


class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [GalleryInline]
    form = GalleryForm
    list_display = ['name', 'order']
    ordering = ['order']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Handling multiple images for Gallery
        images = form.cleaned_data.get('images')
        if images:
            for image in images:
                Gallery.objects.create(course=obj, img=image)


admin.site.register(Course, CourseAdmin)


@admin.register(Certificate)
class CertificateAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order')
    fields = ['img', 'order']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'order')
    fields = ['course', 'img', 'order']
