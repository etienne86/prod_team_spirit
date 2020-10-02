"""Contain the unit tests related to the models in app ``events``."""

import datetime

from django.test import TestCase

from teamspirit.core.models import Address, Location
from teamspirit.events.models import Event


class EventModelTestsCase(TestCase):
    """Test the model ``Event``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address = Address.objects.create(
            label_first="1 rue de l'impasse",
            label_second="",
            postal_code="75000",
            city="Paris",
            country="France"
        )
        cls.location = Location.objects.create(
            name="Salle des fêtes de Paris",
            address=cls.address
        )
        cls.event = Event.objects.create(
            date=datetime.date(2020, 9, 6),
            time=datetime.time(10, 30),
            title="Assemblée Générale de l'association",
            location=cls.location
        )

    def test_event_is_event_instance(self):
        """Unit test - app ``events`` - model ``Event`` - #1.1

        Test that event is an ``Event`` instance.
        """
        self.assertIsInstance(self.event, Event)

    def test_date(self):
        """Unit test - app ``events`` - model ``Event`` - #1.2

        Test the date.
        """
        self.assertIsInstance(self.event.date, datetime.date)
        self.assertEqual(self.event.date, datetime.date(2020, 9, 6))

    def test_time(self):
        """Unit test - app ``events`` - model ``Event`` - #1.3

        Test the time.
        """
        self.assertIsInstance(self.event.time, datetime.time)
        self.assertEqual(self.event.time, datetime.time(10, 30))
