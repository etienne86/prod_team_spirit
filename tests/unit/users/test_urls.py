"""Contain the unit tests related to the urls in app ``users``."""

from django.test import TestCase
from django.urls import reverse


class UsersUrlsTestCase(TestCase):
    """Test the urls in the app ``users``."""

    def test_custom_login_url(self):
        """Unit test - app ``users`` - url ``users/login/``

        Test the login url.
        """
        url = reverse('users:login')
        self.assertEqual(url, '/users/login/')

    def test_custom_logout_url(self):
        """Unit test - app ``users`` - url ``users/logout/``

        Test the logout url.
        """
        url = reverse('users:logout')
        self.assertEqual(url, '/users/logout/')
