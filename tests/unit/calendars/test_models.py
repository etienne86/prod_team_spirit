# """Contain the unit tests related to the models in app ``calendars``."""

# import datetime

# from django.test import TestCase

# from teamspirit.calendars.models import Calendar
# from teamspirit.events.models import Event
# from teamspirit.trainings.models import Training


# class CalendarModelTestsCase(TestCase):
#     """Test the model ``Calendar``."""

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.training = Training.objects.create(

#         )
#         cls.event = Event.objects.create(

#         )
#         cls.calendar = Calendar.objects.create(
#             current_date=datetime.date(2020, 6, 30),
#             period_display="M",

#         )

#     def test_Calendar_is_Calendar_instance(self):
#         """Unit test - app ``Calendars`` - model ``Calendar`` - #1.1

#         Test that Calendar is an ``Calendar`` instance.
#         """
#         self.assertIsInstance(self.Calendar, Calendar)

#     def test_date(self):
#         """Unit test - app ``Calendars`` - model ``Calendar`` - #1.2

#         Test the date.
#         """
#         self.assertIsInstance(self.Calendar.date, datetime.date)
#         self.assertEqual(self.Calendar.date, datetime.date(2020, 9, 6))
