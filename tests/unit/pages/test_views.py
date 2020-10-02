"""Contain the unit tests related to the views in app ``pages``."""

from django.test import TestCase
from django.urls import reverse

from teamspirit.core.models import Address
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class PagesViewsTestCase(TestCase):
    """Test the views in the app ``pages``."""

    def setUp(self):
        super().setUp()
        # a user in database
        self.address = Address.objects.create(
            label_first="1 rue de l'impasse",
            label_second="",
            postal_code="75000",
            city="Paris",
            country="France"
        )
        self.personal = Personal.objects.create(
            phone_number="01 02 03 04 05",
            address=self.address
        )
        self.user = User.objects.create_user(
            email="toto@mail.com",
            first_name="Toto",
            password="TopSecret",
            personal=self.personal
        )
        # log this user in
        self.client.login(email="toto@mail.com", password="TopSecret")

    def test_contact_view(self):
        """Unit test - app ``pages`` - view ``contact_view``

        Test the contact view.
        """
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/contact.html')

    def test_home_view(self):
        """Unit test - app ``pages`` - view ``home_view``

        Test the home view.
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_legal_view(self):
        """Unit test - app ``pages`` - view ``legal_view``

        Test the legal view.
        """
        url = reverse('legal')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/legal.html')
