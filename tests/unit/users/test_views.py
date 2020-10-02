"""Contain the unit tests related to the views in app ``users``."""

from django.test import TestCase
from django.urls import reverse


class UsersViewsTestCase(TestCase):
    """Test the views in the app ``users``."""

    def test_custom_login_view(self):
        """Unit test - app ``users`` - view ``custom_login_view``

        Test the login view.
        """
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_custom_logout_view(self):
        """Unit test - app ``users`` - view ``custom_logout_view``

        Test the logout view.
        """
        url = reverse('users:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/logout.html')
