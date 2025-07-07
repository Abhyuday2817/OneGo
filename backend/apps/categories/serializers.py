from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()
    average_price = serializers.SerializerMethodField()
    has_free_courses = serializers.SerializerMethodField()
    top_course_list = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'type',
            'description',
            'course_count',
            'average_price',
            'has_free_courses',
            'top_course_list',
        ]
        read_only_fields = [
            'id',
            'course_count',
            'average_price',
            'has_free_courses',
            'top_course_list',
        ]

    def get_course_count(self, obj):
        try:
            return obj.total_courses()
        except Exception:
            return 0

    def get_average_price(self, obj):
        try:
            return round(obj.average_price(), 2)
        except Exception:
            return 0.0

    def get_has_free_courses(self, obj):
        try:
            return obj.has_free_courses()
        except Exception:
            return False

    def get_top_course_list(self, obj):
        """
        Returns top 3 courses in this category (for previews).
        Uses CourseCardSerializer from courses app.
        """
        try:
            from apps.courses.serializers import CourseCardSerializer
            qs = obj.top_courses(limit=3)
            return CourseCardSerializer(qs, many=True).data
        except Exception:
            return []
