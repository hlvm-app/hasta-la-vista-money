from django.test import Client, TestCase
from django.urls import reverse_lazy
from faker import Faker
from hasta_la_vista_money.constants import HTTPStatus
from hasta_la_vista_money.users.models import User

LENGTH_PASSWORD = 12


class TestUser(TestCase):
    fixtures = ['users.yaml']

    def setUp(self) -> None:
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.client: Client = Client()
        self.faker = Faker()

    def test_create_user(self):
        self.client.force_login(self.user1)
        self.client.force_login(self.user2)
        url = reverse_lazy('users:registration')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

        Faker.seed(0)
        username = self.faker.user_name()
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self.faker.email()
        set_password = self.faker.password(length=LENGTH_PASSWORD)
        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'policy': True,
            'username': username,
            'password1': set_password,
            'password2': set_password,
        }

        response = self.client.post(url, new_user, follow=True)
        self.assertRedirects(response, '/applications/')
