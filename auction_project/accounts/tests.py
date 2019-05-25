from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework import response
from django.contrib.auth.models import User

from .models import Profile


class RegisterTestCase(APITestCase):
    url = '/accounts/register/'

    def setUp(self):
        self.data = {
            "username": "TestCase_user",
            "password": "123",
            "email": "test@test.te",
            "first_name": "test",
            "last_name": "testov",
            "language": "BG",
        }
        self.client = APIClient()

    def test_register_and_save_user_in_db(self):
        before_save = Profile.objects.count()
        response = self.client.post(self.url, data=self.data,
                                    format='json')
        after_save = Profile.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'Expected status code 201, got {}'.format(
                             response.status_code))

        self.assertEqual(before_save + 1, after_save,
                         'Profile not saving to database')

    def test_password_not_in_response(self):
        response = self.client.post(self.url, data=self.data,
                                    format='json')
        self.assertTrue('password' not in response.data,
                        'Password should not be in the response body.')

    def test_password_storing_in_plaintext(self):

        response = self.client.post(self.url, data=self.data,
                                    format='json')
        profile = Profile.objects.first()
        self.assertNotEqual(profile.user.password,
                            self.data['password'],
                            'Password shoild not be in plaintext')


class LoginTestCase(APITestCase):
    url = '/accounts/auth/login/'

    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "username": "TestCase_user",
            "password": "123",
            "email": "test@test.te",
            "first_name": "test",
            "last_name": "testov"
        }
        self.profile_data = {"language": "BG"}

        self.user = User.objects.create(**self.user_data)
        self.profile = Profile.objects.create(
                user=self.user, **self.profile_data)

    def test_login_valid_credentials(self):
        self.client.force_authenticate(self.user)
        profile = Profile.objects.first()
        get_result = self.client.get('/accounts/' + str(self.user.id) + '/')
        self.assertEqual(get_result.status_code, status.HTTP_200_OK)
