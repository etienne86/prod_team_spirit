from django.urls import path

from teamspirit.trainings.views import trainings_view

app_name = 'trainings'

urlpatterns = [
    path('', trainings_view, name="trainings"),
]
