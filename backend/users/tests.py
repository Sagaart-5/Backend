from django.test import Client, TestCase
from django.urls import reverse_lazy
from rest_framework import status

from .models import CustomUser


valid_user_data = [
    {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "test@email.com",
        "password": "testAdmin123",
        "phone_number": "+79513335203",
    },
    {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "test2@email.com",
        "password": "testAdmin123",
        "phone_number": "+79513335204",
    },
]

invalid_user_data = [
    {
        "last_name": "last_name",
        "email": "test@email.com",
        "password": "testAdmin123",
        "phone_number": "+79513335203",
    },
    {
        "first_name": "first_name",
        "email": "test@email.com",
        "password": "testAdmin123",
        "phone_number": "+79513335203",
    },
    {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "test@email.com",
        "password": "testAdmin123",
        "phone_number": 79513335203,
    },
    {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "test@email.com",
        "password": "testAdmin123",
        "phone_number": "79513335203",
    },
    {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "test@email.com",
        "password": "testAdmin123",
    },
    {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "test@email.com",
        "password": "test",
        "phone_number": "+79513335203",
    },
    {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "t@.com",
        "password": "test",
        "phone_number": "+79513335203",
    },
]


class TestUsers(TestCase):
    user_url = reverse_lazy("users-list")
    jwt_url = reverse_lazy("jwt-create")

    def setUp(self):
        self.client = Client()

    def test_00_get_user_list_unauthorized(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_01_invalid_user_data(self):
        for data in invalid_user_data:
            with self.subTest(msg="Invalid user data", data=data):
                response = self.client.post(
                    self.user_url,
                    data=data,
                )
                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                    response.data,
                )

    def test_02_create_user(self):
        users_count = CustomUser.objects.count()

        response = self.client.post(
            self.user_url,
            data=valid_user_data[0],
        )
        users_count += 1
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), users_count)
        # TODO: Check json response fields

    def test_03_create_jwt_token_and_get_user_list(self):
        self.client.post(
            self.user_url,
            data=valid_user_data[0],
        )
        response = self.client.post(
            self.jwt_url,
            data=valid_user_data[0],
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

        jwt_token = response.json()["access"]
        response = self.client.get(
            self.user_url, headers={"Authorization": f"Bearer {jwt_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: Check json response fields

    def test_04_valid_user_data(self):
        for data in valid_user_data:
            with self.subTest(msg="Valid user data", data=data):
                response = self.client.post(
                    self.user_url,
                    data=data,
                )
                self.assertEqual(
                    response.status_code,
                    status.HTTP_201_CREATED,
                    response.data,
                )
