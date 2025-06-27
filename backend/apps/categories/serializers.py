from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    course_count     = serializers.IntegerField(source='courses.count', read_only=True)
    top_course_list  = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'type', 'description',
            'course_count', 'top_course_list',
        ]
        read_only_fields = ['id', 'course_count', 'top_course_list']

    def get_top_course_list(self, obj):
        # return minimal info on top 3 courses
        from courses.serializers import CourseCardSerializer
        qs = obj.top_courses(limit=3)
        return CourseCardSerializer(qs, many=True).data
