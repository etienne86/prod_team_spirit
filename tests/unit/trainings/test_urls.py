"""Contain the unit tests related to the urls in app ``trainings``."""

from django.test import TestCase
from django.urls import reverse


class TrainingsUrlsTestCase(TestCase):
    """Test the urls in the app ``trainings``."""

    def test_trainings_url(self):
        """Unit test - app ``trainings`` - url ``/trainings/``

        Test the trainings url.
        """
        url = reverse('trainings:trainings')
        self.assertEqual(url, '/trainings/')
