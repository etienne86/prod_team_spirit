"""Contain the integration tests in app ``catalogs``."""

from django.test import TestCase
from django.urls import reverse

from teamspirit.core.models import Address
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class CatalogsIntegrationTestCase(TestCase):
    """Test integration in the app ``catalogs``."""

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

    def test_catalog_view_with_url(self):
        """Integration test - app ``catalogs`` - view with url

        Test the catalog view with url.
        """
        url = reverse('catalogs:catalog')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogs/catalog.html')
