from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class ContactView(TemplateView):

    template_name = "pages/contact.html"


contact_view = ContactView.as_view()
contact_view = login_required(contact_view)


class HomeView(TemplateView):

    template_name = "pages/home.html"


home_view = HomeView.as_view()
home_view = login_required(home_view)


class LegalView(TemplateView):

    template_name = "pages/legal.html"


legal_view = LegalView.as_view()
legal_view = login_required(legal_view)
