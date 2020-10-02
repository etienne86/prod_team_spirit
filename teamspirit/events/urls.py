from django.urls import path

from teamspirit.events.views import events_view

app_name = 'events'

urlpatterns = [
    path('', events_view, name="events"),
]
