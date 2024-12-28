from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name_en', 'course_name_fa', 'professor', 'faculty', 'exam_date')
    search_fields = ('course_name_en', 'course_name_fa')