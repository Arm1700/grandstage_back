from django import forms
from multiupload.fields import MultiImageField
from .models import Gallery


class GalleryForm(forms.ModelForm):
    # img = MultiImageField(required=True, min_num=1, max_num=100, max_file_size=1024 * 1024 * 100)

    class Meta:
        model = Gallery
        fields = ['course', 'img']
