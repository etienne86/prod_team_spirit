from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms as django_forms
from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from teamspirit.users.models import User


class UserChangeForm(forms.UserChangeForm):

    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name")
        field_classes = {
            'email': django_forms.EmailField,
            'first_name': django_forms.CharField,
            'last_name': django_forms.CharField
        }


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_email": _("This email has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {'email': django_forms.EmailField}

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])


class CustomAuthenticationForm(forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-authentication-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit', 'Se connecter'))
