"""Contain the models related to the app ``trainings``."""

from django.db import models

from teamspirit.core.models import Location
from teamspirit.profiles.models import Personal
from teamspirit.trainings.managers import TrainingManager


class Training(models.Model):
    """Define a training session."""

    DAYS = [
        (1, "Lundi"),
        (2, "Mardi"),
        (3, "Mercredi"),
        (4, "Jeudi"),
        (5, "Vendredi"),
        (6, "Samedi"),
        (7, "Dimanche"),
    ]

    is_weekly = models.BooleanField(
        verbose_name="Entraînement hebdomadaire",
        default="False"
    )
    date = models.DateField(
        verbose_name="Date de l'entraînement",
        null=True
    )
    day = models.IntegerField(
        choices=DAYS,
        verbose_name="Jour de l'entraînement",
        null=True
    )
    time = models.TimeField(verbose_name="Début de l'entraînement")
    trainer = models.ForeignKey(
        to=Personal,
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        to=Location,
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=100)
    note = models.CharField(max_length=1000)

    objects = TrainingManager()
