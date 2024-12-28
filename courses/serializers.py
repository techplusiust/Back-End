from rest_framework import serializers
from .models import Course
from professors.models import Professor

class CourseSerializer(serializers.ModelSerializer):
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'course_name_fa', 'course_name_en', 'professor', 'professor_name', 'faculty',
            'first_day_of_week', 'first_day_time', 'first_day_duration',
            'second_day_of_week', 'second_day_time', 'second_day_duration',
            'exam_date', 'exam_start_time', 'exam_duration'
        ]
        read_only_fields = ['professor_name']

    def get_professor_name(self, obj):
        """Retrieve the professor's name for display."""
        return f"{obj.professor.name_en} ({obj.professor.name_fa})"

    def validate_faculty(self, value):
        """Ensure the faculty exists in the professors database."""
        valid_faculties = Professor.objects.values_list('department_en', flat=True).distinct()
        if value not in valid_faculties:
            raise serializers.ValidationError(f"Faculty '{value}' does not exist in the professors database.")
        return value
