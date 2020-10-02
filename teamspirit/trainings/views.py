from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class TrainingsView(TemplateView):

    template_name = "trainings/trainings.html"


trainings_view = TrainingsView.as_view()
trainings_view = login_required(trainings_view)
