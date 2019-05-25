from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework import response
from django.contrib.auth.models import User

from .models import Profile

"""
Register testing is not working. TODO - update to work

class RegisterTestCase(APITestCase):
    url = '/accounts/register/'

    def setUp(self):
        self.data = {
            "user": {
                "username": "user_test",
                "password": "password_test",
                "first_name": "name_test",
                "last_name": "last_name_test",
                "email": "test@test.te"
            },
            "language": "English"
        }
        self.client = APIClient()

    def test_register_and_save_user_in_db(self):
        before_save = Profile.objects.count()
        response = self.client.post(self.url, data=self.data,
                                    format='json')
        after_save = Profile.objects.count()
        # import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'Expected status code 201, got {}'.format(
                             response.status_code))

        self.assertEqual(before_save + 1, after_save,
                         'Profile not saving to database')

    def test_password_not_in_response(self):
        response = self.client.post(self.url, data=self.data,
                                    format='json')
        # import ipdb; ipdb.set_trace()
        self.assertTrue('password' not in response.data,
                        'Password should not be in the response body.')

    def test_password_storing_in_plaintext(self):
        response = self.client.post(self.url, data=self.data,
                                    format='json')
        profile = Profile.objects.first()
        self.assertNotEqual(profile.user.password,
                            self.data['user']['password'],
                            'Password shoild not be in plaintext')


class LoginTestCase(APITestCase):
    url = '/accounts/auth/login/'

    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "username": "user_test",
            "password": "password_test",
            "first_name": "name_test",
            "last_name": "last_name_test",
            "email": "test@test.te"
            }
        self.profile_data = {"language": "BG"}
        
        self.user = User.objects.create(**self.user_data)
        self.profile = Profile.objects.create(user=user, **self.profile_data)
"""