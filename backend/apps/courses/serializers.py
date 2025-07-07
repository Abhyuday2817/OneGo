from rest_framework import serializers
from django.utils.timesince import timesince
from django.db.models import Avg
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.db.models.expressions import RawSQL

from .models import Course
from apps.categories.serializers import CategorySerializer
from apps.mentors.serializers import MentorProfileSerializer
from apps.enrollments.models import Enrollment


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    mentor = MentorProfileSerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Course._meta.get_field('category').related_model.objects.all(),
        source='category', write_only=True
    )
    mentor_id = serializers.PrimaryKeyRelatedField(
        queryset=Course._meta.get_field('mentor').related_model.objects.all(),
        source='mentor', write_only=True
    )

    mentor_username = serializers.CharField(source="mentor.user.username", read_only=True)
    enrolled_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    time_since_created = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description',
            'category', 'category_id',
            'price', 'delivery_type',
            'mentor', 'mentor_id', 'mentor_username',
            'schedule_info', 'duration_hours',
            'preview_video', 'intro_pdf',
            'created_at', 'updated_at',
            'enrolled_count', 'average_rating',
            'time_since_created'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'category', 'mentor', 'mentor_username',
            'enrolled_count', 'average_rating', 'time_since_created'
        ]

    def get_enrolled_count(self, obj):
        return Enrollment.objects.filter(course=obj).count()

    def get_average_rating(self, obj):
        qs = Enrollment.objects.filter(course=obj, completed=True)
        avg_rating = qs.annotate(
            rating_num=Cast(
                RawSQL("(progress ->> 'rating')::float", (), output_field=FloatField()),
                output_field=FloatField()
            )
        ).aggregate(avg=Avg('rating_num'))['avg'] or 0.0
        return round(avg_rating, 2)

    def get_time_since_created(self, obj):
        return timesince(obj.created_at) + " ago"

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be zero or positive.")
        return value

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
