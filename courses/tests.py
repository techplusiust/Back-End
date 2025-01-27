from django.test import TestCase
# courses/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from professors.models import Professor
from accounts.models import CustomUser
from .models import Course


class CourseAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and a professor for testing
        self.user = CustomUser.objects.create_user(
            email="user@example.com",
            password="password123",
            fullname="Test User",
            national_code="1234567890",
            student_number="987654321",
        )
        self.professor = Professor.objects.create(
            name_en="John Doe",
            name_fa="جان دو",
            department_en="Computer Science",
            department_fa="علوم کامپیوتر"
        )
        self.client.login(email="user@example.com", password="password123")

        # Define a sample course payload
        self.course_data = {
            "course_name_fa": "ریاضی",
            "course_name_en": "Mathematics",
            "professor_id": self.professor,
            "faculty_fa": "علوم",
            "faculty_en": "Science",
            "first_day_of_week": 0,
            "first_day_time": "09:00",
            "first_day_duration": 1.5,
            "second_day_of_week": 2,
            "second_day_time": "10:00",
            "second_day_duration": 1.5,
            "exam_date": "2025-02-20",
            "exam_start_time": "08:30",
            "exam_duration": 2.0,
        }
        self.list_url = reverse("course-list")

    def test_create_course(self):
        """Test creating a course."""
        req_data = self.course_data
        req_data['professor_id'] = self.professor.id
        response = self.client.post(self.list_url, req_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.first().course_name_en, "Mathematics")

    def test_get_courses(self):
        """Test retrieving a list of courses."""
        Course.objects.create(**self.course_data)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["course_name_en"], "Mathematics")

    def test_filter_courses_by_faculty(self):
        """Test filtering courses by faculty."""
        Course.objects.create(**self.course_data)
        response = self.client.get(self.list_url, {"faculty_fa": "علوم"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_partial_update_course(self):
        """Test partially updating a course."""
        course = Course.objects.create(**self.course_data)
        url = reverse("course-detail", args=[course.id])
        response = self.client.patch(url, {"course_name_en": "Advanced Mathematics"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.course_name_en, "Advanced Mathematics")

    def test_delete_course(self):
        """Test deleting a course."""
        course = Course.objects.create(**self.course_data)
        url = reverse("course-detail", args=[course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

# Create your tests here.
