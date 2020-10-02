"""Contain the unit tests related to the views in app ``catalogs``."""

from django.http.request import HttpRequest
from django.test import TestCase

from teamspirit.catalogs.views import catalog_view
from teamspirit.core.models import Address
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class CatalogsViewsTestCase(TestCase):
    """Test the views in the app ``catalogs``."""

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
        # a 'get' request
        self.get_request = HttpRequest()
        self.get_request.method = 'get'
        self.get_request.user = self.user

    def test_catalog_view(self):
        """Unit test - app ``catalogs`` - view ``catalog_view``

        Test the catalog view.
        """
        view = catalog_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Team Spirit - Catalogue</title>', html)
