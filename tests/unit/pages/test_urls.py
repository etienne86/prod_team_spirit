"""Contain the unit tests related to the urls in app ``pages``."""

from django.test import TestCase
from django.urls import reverse


class PagesUrlsTestCase(TestCase):
    """Test the urls in the app ``pages``."""

    def test_contact_url(self):
        """Unit test - app ``pages`` - url ``/contact/``

        Test the contact url.
        """
        url = reverse('contact')
        self.assertEqual(url, '/contact/')

    def test_home_url(self):
        """Unit test - app ``pages`` - url ``/``

        Test the home url.
        """
        url = reverse('home')
        self.assertEqual(url, '/')

    def test_legal_url(self):
        """Unit test - app ``pages`` - url ``/legal/``

        Test the legal url.
        """
        url = reverse('legal')
        self.assertEqual(url, '/legal/')
