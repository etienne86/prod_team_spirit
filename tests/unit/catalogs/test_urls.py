"""Contain the unit tests related to the urls in app ``catalogs``."""

from django.test import TestCase
from django.urls import reverse


class CatalogsUrlsTestCase(TestCase):
    """Test the urls in the app ``catalogs``."""

    def test_catalog_url(self):
        """Unit test - app ``catalogs`` - url ``catalog/``

        Test the catalog url.
        """
        url = reverse('catalogs:catalog')
        self.assertEqual(url, '/catalog/')
