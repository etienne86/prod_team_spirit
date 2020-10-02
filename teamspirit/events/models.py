"""Contain the models related to the app ``events``."""

from django.db import models

# from teamspirit.calendars.models import Calendar
from teamspirit.core.models import Location
from teamspirit.events.managers import EventManager


class Event(models.Model):
    """Define an event."""

    date = models.DateField(verbose_name="Date de l'entraînement")
    time = models.TimeField(verbose_name="Début de l'entraînement")
    title = models.CharField(
        max_length=100,
        unique=True
    )
    location = models.ForeignKey(
        to=Location,
        on_delete=models.CASCADE
    )
    # attached_files = models.ManyToManyField(
    #     to=File,
    #     related_name="events",
    #     on_delete=models.SET_NULL,
    #     blank=True
    # )
    # calendar = models.ForeignKey(
    #     to=Calendar,
    #     on_delete=models.CASCADE
    # )

    objects = EventManager()
