from django.db import models
from professors.models import Professor  # Ensure correct import path
from accounts.models import CustomUser  # Import the CustomUser model
from django.core.exceptions import ValidationError

def validate_time_format(value):
    """Ensure the time is in HH:MM format and within valid ranges."""
    try:
        # Split the value into hours and minutes
        hour, minute = map(int, value.split(":"))
        # Validate the ranges
        if not (0 <= hour <= 23):
            raise ValidationError("Hour must be between 0 and 23.")
        if not (0 <= minute <= 59):
            raise ValidationError("Minute must be between 0 and 59.")
    except ValueError:
        # Raise an error if the value cannot be split or converted
        raise ValidationError("Time must be in HH:MM format.")


class Course(models.Model):
    course_name_fa = models.CharField(max_length=255, verbose_name="Course Name (Persian)")
    course_name_en = models.CharField(max_length=255, verbose_name="Course Name (English)")
    professor_id = models.ForeignKey(Professor, related_name="courses", on_delete=models.CASCADE)
    faculty_fa = models.CharField(max_length=255, verbose_name="Faculty Persian")
    faculty_en = models.CharField(max_length=255, verbose_name="Faculty English")
    
    # Schedule for two days
    first_day_of_week = models.PositiveSmallIntegerField(
        verbose_name="First Day of Week",
        help_text="0: Sunday, 6: Saturday"
    )
    first_day_time = models.CharField(
        max_length=5, 
        verbose_name="First Day Time",
        validators=[validate_time_format],
        help_text="Format: HH:MM (24-hour format)"
    )
    first_day_duration = models.FloatField(verbose_name="First Day Duration (hours)")

    second_day_of_week = models.PositiveSmallIntegerField(
        verbose_name="Second Day of Week",
        help_text="0: Sunday, 6: Saturday"
    )
    second_day_time = models.CharField(
        max_length=5,
        verbose_name="Second Day Time",
        validators=[validate_time_format], 
        help_text="Format: HH:MM (24-hour format)"
    )
    second_day_duration = models.FloatField(verbose_name="Second Day Duration (hours)")


    # Exam details
    exam_date = models.DateField(verbose_name="Exam Date")
    exam_start_time = models.CharField(
        max_length=5, 
        verbose_name="Exam Start Time",
        validators=[validate_time_format],
        help_text="Format: HH:MM (24-hour format)"
    )    
    exam_duration = models.FloatField(verbose_name="Exam Duration (hours)")

    def __str__(self):
        return f"{self.course_name_en} / {self.course_name_fa} ({self.faculty_fa} / {self.faculty_en})"
  
  
    def clean(self):
        """Ensure the faculty exists in the professors database."""
        from django.core.exceptions import ValidationError

        # Check if the faculty exists in Professor
        valid_faculties = Professor.objects.values_list("department_en", flat=True).distinct()
        if self.faculty not in valid_faculties:
            raise ValidationError(f"Faculty '{self.faculty}' does not exist in the professors database.")