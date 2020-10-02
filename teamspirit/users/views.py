from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from teamspirit.users.forms import CustomAuthenticationForm
from teamspirit.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "email"
    slug_url_kwarg = "email"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["email", "first_name", "last_name"]

    def get_success_url(self):
        return reverse(
            "users:detail", kwargs={"email": self.request.user.email}
        )

    def get_object(self):
        return User.objects.get(email=self.request.user.email)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("home")


user_redirect_view = UserRedirectView.as_view()


class CustomLoginView(LoginView):

    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm


custom_login_view = CustomLoginView.as_view()


class CustomLogoutView(LogoutView):

    template_name = 'users/logout.html'


custom_logout_view = CustomLogoutView.as_view()
