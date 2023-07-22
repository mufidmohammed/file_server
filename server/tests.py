from django.test import TestCase

# Create your tests here.
# tests.py
from django.test import TestCase
from django.urls import reverse
from .models import User


class UserLoginTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'test2user',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }
        # Create a user using the custom user model
        self.user = User.objects.create_user(**self.user_data)

    def test_login_view(self):
        # Ensure the login view returns HTTP 200 (OK) status code
        response = self.client.get(reverse('server:login'))
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        # Ensure the user can log in with correct credentials
        response = self.client.post(reverse('server:login'), self.user_data)
        # Check that the login redirects to the success page or URL after login
        self.assertRedirects(response, reverse('server:index'))

    def test_unsuccessful_login(self):
        # Ensure the user cannot log in with incorrect credentials
        wrong_credentials = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword123',
        }
        response = self.client.post(reverse('server:login'), wrong_credentials)
        # Check that the login page is rendered again with the correct status code
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the 'form' context with errors
        self.assertTrue('message' in response.context)
        # self.assertTrue(response.context['form'].errors)


class UserSignupTest(TestCase):
    def setUp(self):
        self.signup_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

    def test_signup_view(self):
        # Ensure the signup view returns HTTP 200 (OK) status code
        response = self.client.get(reverse('server:register'))
        self.assertEqual(response.status_code, 200)

    def test_successful_signup(self):
        # Ensure a new user can sign up successfully
        response = self.client.post(reverse('server:register'), self.signup_data)
        # Check that the signup redirects to the login page after signup
        self.assertRedirects(response, reverse('server:login'))

        # Check that the user is created in the database
        user = User.objects.filter(email=self.signup_data['email'])
        self.assertTrue(user.exists())

    def test_unsuccessful_signup(self):
        # Ensure a user cannot sign up with incomplete or invalid data
        incomplete_data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': '',  # Password confirmation missing
        }
        response = self.client.post(reverse('server:register'), incomplete_data)
        # Check that the signup page is rendered again with appropriate form errors
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the 'form' context with errors
        self.assertTrue('form' in response.context)
        self.assertTrue(response.context['form'].errors)

