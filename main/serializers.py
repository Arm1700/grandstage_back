from rest_framework import serializers
from .models import Course, Gallery, Event, Outcome, EventGallery


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'img', 'order']


class EventGallerySerializer(serializers.ModelSerializer):
    event_gallery_name = serializers.CharField(source='event.name', read_only=True)

    class Meta:
        model = EventGallery
        fields = ['id', 'event', 'event_gallery_name', 'img', 'order']


class GallerySerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Gallery
        fields = ['id', 'course', 'course_name', 'img', 'order']


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ['id', 'text', 'order']


class EventSerializer(serializers.ModelSerializer):
    outcomes = OutcomeSerializer(many=True, required=False)
    event_galleries = EventGallerySerializer(many=True,  required=False)

    class Meta:
        model = Event
        fields = ['id', 'day', 'month', 'title', 'hour', 'place', 'event_description', 'description', 'image', 'status',
                  'order', 'outcomes', 'event_galleries']

    def create(self, validated_data):
        outcomes_data = validated_data.pop('outcomes', [])
        event = Event.objects.create(**validated_data)
        for outcome_data in outcomes_data:
            Outcome.objects.create(event=event, **outcome_data)
        return event

    def update(self, instance, validated_data):
        outcomes_data = validated_data.pop('outcomes', [])
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Обновите или создайте результаты
        for outcome_data in outcomes_data:
            outcome_id = outcome_data.get('id', None)
            if outcome_id:
                outcome = Outcome.objects.get(id=outcome_id, event=instance)
                outcome.text = outcome_data.get('text', outcome.text)
                outcome.order = outcome_data.get('order', outcome.order)
                outcome.save()
            else:
                Outcome.objects.create(event=instance, **outcome_data)

        return instance


class CourseSerializer(serializers.ModelSerializer):
    galleries = GallerySerializer(many=True, source='gallery_set')

    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'order', 'desc', 'galleries']


class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()
