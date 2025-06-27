from rest_framework import serializers
from .models import Course
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer
from apps.mentors.models import MentorProfile
from apps.mentors.serializers import MentorProfileSerializer
from apps.enrollments.models import Enrollment

class CourseSerializer(serializers.ModelSerializer):
    # Nested read-only representations
    category = CategorySerializer(read_only=True)
    mentor = MentorProfileSerializer(read_only=True)
    mentor_username = serializers.CharField(source="mentor.user.username", read_only=True)

    # PK fields for writes
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    mentor_id = serializers.PrimaryKeyRelatedField(
        queryset=MentorProfile.objects.all(),
        source='mentor',
        write_only=True
    )

    # Derived fields
    related_courses = serializers.SerializerMethodField()
    enrolled_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description',
            'category', 'category_id',
            'price', 'delivery_type',
            'mentor', 'mentor_id', 'mentor_username',
            'schedule_info',
            'created_at', 'updated_at',
            'related_courses', 'enrolled_count',
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'related_courses', 'enrolled_count',
            'category', 'mentor', 'mentor_username',
        ]

    def get_related_courses(self, obj):
        """
        Return up to 3 other courses in the same category,
        ordered by price descending (as a proxy for popularity).
        """
        qs = obj.related(limit=3)
        return CourseSerializer(qs, many=True, context=self.context).data

    def get_enrolled_count(self, obj):
        """
        Count how many Enrollment records point to this course.
        """
        return Enrollment.objects.filter(course=obj).count()

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
