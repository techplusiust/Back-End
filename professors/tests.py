from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Professor, Comment
from accounts.models import CustomUser


class ProfessorsAppAPITests(APITestCase):

    def setUp(self):
        # Create a test user with email, and password
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",  # Provide email as required
            password="password"
        )
        self.professor = Professor.objects.create(
            name_fa="استاد تست",
            name_en="Test Professor",
            department_fa="مهندسی کامپیوتر",
            department_en="Computer Engineering"
        )
        self.client.login(email="testuser@example.com", password="password")

    def test_get_all_professors(self):
        """Test retrieving all professors"""
        response = self.client.get('/api/professors/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data[0])  # Check if 'name' field exists in response

    def test_get_professor_with_comments(self):
        """Test retrieving professor data along with their comments"""
        # Add a comment to professor
        Comment.objects.create(
            professor=self.professor,
            user=self.user,
            text="Great professor!"
        )
        response = self.client.get(f'/api/professors/{self.professor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['comments']), 1)  # Check if comment is present

    def test_add_comment_authenticated_user(self):
        """Test adding a comment by an authenticated user"""
        response = self.client.post('/api/professors/add_comment/', {
            "professor_id": self.professor.id,
            "text": "Amazing class!"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)  # Ensure one comment has been added
        self.assertEqual(Comment.objects.first().text, "Amazing class!")  # Verify the comment's text

    def test_add_comment_unauthenticated_user(self):
        """Test adding a comment without authentication (should fail)"""
        self.client.logout()  # Log out the current user
        response = self.client.post('/api/professors/add_comment/', {
            "professor_id": self.professor.id,
            "text": "Unauthorized comment!"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Check for unauthorized status

    def test_faculty_list(self):
        """Test getting the list of distinct faculties"""
        response = self.client.get('/api/professors/faculties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("faculties", response.data)  # Check if faculties key exists in the response
        self.assertEqual(len(response.data["faculties"]), 1)  # Check if there is one faculty in the list

# Create your tests here.
