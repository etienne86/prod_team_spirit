from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class EventsView(TemplateView):

    template_name = "events/events.html"


events_view = EventsView.as_view()
events_view = login_required(events_view)
