from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class UserAPITestCase(APITestCase):
    def setUp(self):
        # Create a superuser and regular user for testing
        self.superuser = get_user_model().objects.create_superuser(
            email="superuser@test.com",
            password="superpass",
            fullname="Super User",
            national_code="1234567890",
            student_number="S12345",
            department="IT"
        )
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="userpass",
            fullname="Regular User",
            national_code="9876543210",
            student_number="S54321",
            department="HR"
        )
        self.superuser_token = Token.objects.create(user=self.superuser)
        self.user_token = Token.objects.create(user=self.user)

    def test_signup(self):
        data = {
            "fullname": "New User",
            "national_code": "1122334455",
            "email": "newuser@test.com",
            "department": "Engineering",
            "student_number": "S11111",
            "password1": "newuserpass",
            "password2": "newuserpass",
        }
        response = self.client.post("/api/accounts/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_login(self):
        data = {"email": "user@test.com", "password": "userpass"}
        response = self.client.post("/api/accounts/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_get_all_users_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.superuser_token.key)
        response = self.client.get("/api/accounts/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_get_all_users_as_non_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.get("/api/accounts/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        data = {"fullname": "Updated Regular User"}
        response = self.client.put(f"/api/accounts/users/{self.user.id}/edit/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.fullname, "Updated Regular User")

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.superuser_token.key)
        response = self.client.delete(f"/api/accounts/users/{self.user.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(id=self.user.id)

    def test_make_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.superuser_token.key)
        response = self.client.post(f"/api/accounts/users/{self.user.id}/make-superuser/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_superuser)

    def test_cannot_make_superuser_as_non_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(f"/api/accounts/users/{self.user.id}/make-superuser/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_self_delete_not_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.delete(f"/api/accounts/users/{self.user.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_cannot_be_deleted(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.superuser_token.key)
        response = self.client.delete(f"/api/accounts/users/{self.superuser.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_test_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.get("/api/accounts/test_token/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Create your tests here.
