from rest_framework import serializers
from .models import Course, Gallery


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'img', 'order']


class GallerySerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Gallery
        fields = ['id', 'course', 'course_name', 'img', 'order']


class CourseSerializer(serializers.ModelSerializer):
    galleries = GallerySerializer(many=True, source='gallery_set')

    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'order', 'desc', 'galleries']


class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()
