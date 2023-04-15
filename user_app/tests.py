from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):

    def test_register(self):

        data = {
            "username": "aryanTesting",
            "email": "aryantesting1@gmail.com",
            "password": "1313",
            "password2": "1313",
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Registration failing')


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="UserTest", password="1313")

    def test_login(self):
        data = {
            "username": "UserTest",
            "password": "1313"
        }

        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Login failing')

    def test_logout(self):
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Logout failing')