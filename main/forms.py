from django import forms
from main.models import Course, Event


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class GalleryForm(forms.ModelForm):
    images = MultipleFileField(label='Select files for Gallery', required=False)

    class Meta:
        model = Course  # Targeting the Course model for the form
        fields = ['name', 'image', 'order', 'desc']  # Fields for Course
        widgets = {
            'images': MultipleFileInput(),
        }


class EventGalleryForm(forms.ModelForm):
    images = MultipleFileField(label='Select files for Event Gallery', required=False)

    class Meta:
        model = Event  # Targeting the Course model for the form
        fields = ['day', 'month', 'title', 'hour', 'place', 'event_description', 'description', 'image', 'status',
                  'order']  # Fields for Course
        widgets = {
            'images': MultipleFileInput(),
        }