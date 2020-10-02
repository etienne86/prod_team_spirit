"""Contain the unit tests related to the views in app ``trainings``."""

from django.test import TestCase
from django.urls import reverse

from teamspirit.core.models import Address
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class TrainingsViewsTestCase(TestCase):
    """Test the views in the app ``trainings``."""

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

    def test_catalog_view(self):
        """Unit test - app ``trainings`` - view ``trainings_view``

        Test the catalog view.
        """
        url = reverse('trainings:trainings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainings/trainings.html')
