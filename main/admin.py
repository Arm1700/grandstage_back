from django.contrib import admin
from .forms import GalleryForm, EventGalleryForm
from .models import Course, Gallery, Certificate, Event, Outcome, EventGallery
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


class GalleryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Gallery
    extra = 0
    fields = ['img', 'order']
    sortable_field_name = "order"


class OutcomeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Outcome
    extra = 0
    fields = ['text', 'order']
    sortable_field_name = "order"


class EventGalleryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = EventGallery
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


@admin.register(Event)
class EventAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [OutcomeInline, EventGalleryInline]
    form = EventGalleryForm
    list_display = ['day', 'title', 'month', 'hour', 'place', 'status', 'order']
    field = '__all__'
    search_fields = ['title', 'event_description']
    list_filter = ['status']
    ordering = ['order']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Handling multiple images for Gallery
        images = form.cleaned_data.get('images')
        if images:
            for image in images:
                EventGallery.objects.create(event=obj, img=image)

