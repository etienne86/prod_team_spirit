# """Contain the models related to the app ``calendars``."""

# import datetime

# from django.db import models
# from django.utils.translation import ugettext_lazy as _

# from teamspirit.calendars.managers import CalendarManager
# from teamspirit.trainings.models import Training


# class Calendar(models.Model):
#     """Define a calendar."""

#     PERIODS = [
#         ("D", _("Day")),
#         ("W", _("Week")),
#         ("M", _("Month")),
#         ("Y", _("Year")),
#     ]

#     current_date = models.DateField(default=datetime.date.today())
#     period_display = models.CharField(
#         choices=PERIODS,
#         max_length=1,
#         verbose_name=_("Display mode")
#     )

#     objects = CalendarManager()
