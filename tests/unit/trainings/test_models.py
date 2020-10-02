"""Contain the unit tests related to the models in app ``trainings``."""

import datetime

from django.test import TestCase

from teamspirit.core.models import Address, Location
from teamspirit.profiles.models import Personal
from teamspirit.trainings.models import Training


class TrainingModelTestsCase(TestCase):
    """Test the model ``Training``."""

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
        cls.trainer = Personal.objects.create(
            phone_number="01 02 03 04 05",
            address=cls.address
        )
        cls.location = Location.objects.create(
            name="Chez Coach",
            address=cls.address
        )
        cls.weekly_training = Training.objects.create(
            is_weekly=True,
            day=7,
            time=datetime.time(9, 0),
            trainer=cls.trainer,
            location=cls.location,
            content="1h d'endurance",
            note="allure environ 6'/km"
        )
        cls.one_off_training = Training.objects.create(
            is_weekly=False,
            date=datetime.date(2020, 6, 14),
            time=datetime.time(9, 0),
            trainer=cls.trainer,
            location=cls.location,
            content="1h d'endurance",
            note="allure environ 6'/km"
        )

    def test_training_is_training_instance(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.1

        Test that training is a ``Training`` instance.
        """
        self.assertIsInstance(self.weekly_training, Training)
        self.assertIsInstance(self.one_off_training, Training)

    def test_weekly_training_is_weekly(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.2

        Test that the weekly training is weekly.
        """
        self.assertIsInstance(self.weekly_training.is_weekly, bool)
        self.assertTrue(self.weekly_training.is_weekly)

    def test_one_off_training_is_not_weekly(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.3

        Test that the one_off training is not weekly.
        """
        self.assertIsInstance(self.one_off_training.is_weekly, bool)
        self.assertFalse(self.one_off_training.is_weekly)

    def test_weekly_training_day(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.4

        Test the day of the weekly training.
        """
        self.assertIsInstance(self.weekly_training.day, int)
        self.assertEqual(self.weekly_training.day, 7)

    def test_one_off_training_date(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.5

        Test the date of the one_off training.
        """
        self.assertIsInstance(self.one_off_training.date, datetime.date)
        self.assertEqual(
            self.one_off_training.date,
            datetime.date(2020, 6, 14)
        )

    def test_training_time(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.6

        Test the time of the training.
        """
        self.assertIsInstance(self.one_off_training.time, datetime.time)
        self.assertEqual(self.one_off_training.time, datetime.time(9, 0))

    def test_training_trainer(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.7

        Test the trainer of the training.
        """
        self.assertIsInstance(self.one_off_training.trainer, Personal)
        self.assertEqual(self.one_off_training.trainer, self.trainer)

    def test_training_location(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.8

        Test the location of the training.
        """
        self.assertIsInstance(self.one_off_training.location, Location)
        self.assertEqual(self.one_off_training.location, self.location)

    def test_training_content(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.9

        Test the content of the training.
        """
        self.assertIsInstance(self.one_off_training.content, str)
        self.assertEqual(self.one_off_training.content, "1h d'endurance")

    def test_training_note(self):
        """Unit test - app ``trainings`` - model ``Training`` - #1.9

        Test the note of the training.
        """
        self.assertIsInstance(self.one_off_training.note, str)
        self.assertEqual(self.one_off_training.note, "allure environ 6'/km")
