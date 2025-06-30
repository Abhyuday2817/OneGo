from rest_framework import serializers
from .models import Course, CourseQuiz
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer
from apps.mentors.models import MentorProfile
from apps.mentors.serializers import MentorProfileSerializer
from apps.enrollments.models import Enrollment


class CourseQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseQuiz
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # Nested serializers
    category = CategorySerializer(read_only=True)
    mentor = MentorProfileSerializer(read_only=True)
    quizzes = CourseQuizSerializer(many=True, read_only=True)

    # Derived fields
    mentor_username = serializers.CharField(source="mentor.user.username", read_only=True)
    related_courses = serializers.SerializerMethodField()
    enrolled_count = serializers.SerializerMethodField()

    # Writable PKs
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

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description',
            'category', 'category_id',
            'price', 'delivery_type',
            'mentor', 'mentor_id', 'mentor_username',
            'schedule_info', 'duration_hours',
            'preview_video', 'intro_pdf', 'certificate_available',
            'created_at', 'updated_at',
            'related_courses', 'enrolled_count',
            'quizzes'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'related_courses', 'enrolled_count',
            'category', 'mentor', 'mentor_username', 'quizzes'
        ]

    def get_related_courses(self, obj):
        """
        Return up to 3 other courses in the same category.
        """
        qs = obj.related(limit=3)
        return CourseSerializer(qs, many=True, context=self.context).data

    def get_enrolled_count(self, obj):
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
