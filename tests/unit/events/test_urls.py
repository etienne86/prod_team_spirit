"""Contain the unit tests related to the urls in app ``events``."""

from django.test import TestCase
from django.urls import reverse


class EventsUrlsTestCase(TestCase):
    """Test the urls in the app ``events``."""

    def test_events_url(self):
        """Unit test - app ``events`` - url ``/events/``

        Test the events url.
        """
        url = reverse('events:events')
        self.assertEqual(url, '/events/')
