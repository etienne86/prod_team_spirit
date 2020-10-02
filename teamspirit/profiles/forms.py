from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django.contrib.auth import forms as auth_forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from teamspirit.core.models import Address
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-change-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', _('Change password')))


class CustomPasswordResetForm(auth_forms.PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-reset-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', _('Reset my password')))


class CustomSetPasswordForm(auth_forms.SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-set-password-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', _('Set Password')))


class PersonalInfoForm(ModelForm):

    class Meta:
        model = User
        fields = ['last_name', 'first_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PersonalInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-update-personal-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('last_name', value=self.user.last_name),
            Field('first_name', value=self.user.first_name)
        )
        self.helper.add_input(Submit('submit', 'Mettre à jour'))
        if self.is_valid():
            self.save()

    def save(self, commit=True):
        last_name = self.cleaned_data["last_name"]
        first_name = self.cleaned_data["first_name"]
        if commit:
            self.user.last_name = last_name.upper()
            self.user.first_name = first_name.capitalize()
            self.user.save()
        return self.user


class PhoneForm(ModelForm):

    class Meta:
        model = Personal
        fields = ['phone_number']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PhoneForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-update-phone-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        phone_number = self.user.personal.phone_number
        if phone_number:
            field_phone_number = Field('phone_number', value=phone_number)
        else:
            field_phone_number = Field('phone_number')
        self.helper.layout = Layout(field_phone_number)

    def save(self, commit=True):
        phone_number = self.cleaned_data["phone_number"]
        if commit:
            self.user.personal.phone_number = phone_number
            self.user.personal.save()
        return self.user.personal


class AddressForm(ModelForm):

    class Meta:
        model = Address
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-update-address-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        label_first = self.user.personal.address.label_first
        label_second = self.user.personal.address.label_second
        postal_code = self.user.personal.address.postal_code
        city = self.user.personal.address.city
        country = self.user.personal.address.country
        if label_first:
            field_label_first = Field('label_first', value=label_first)
        else:
            field_label_first = Field('label_first')
        if label_second:
            field_label_second = Field('label_second', value=label_second)
        else:
            field_label_second = Field('label_second')
        if postal_code:
            field_postal_code = Field('postal_code', value=postal_code)
        else:
            field_postal_code = Field('postal_code')
        if city:
            field_city = Field('city', value=city)
        else:
            field_city = Field('city')
        if country:
            field_country = Field('country', value=country)
        else:
            field_country = Field('country')
        self.helper.layout = Layout(
            field_label_first,
            field_label_second,
            field_postal_code,
            field_city,
            field_country,
        )

    def save(self, commit=True):
        label_first = self.cleaned_data["label_first"]
        label_second = self.cleaned_data["label_second"]
        postal_code = self.cleaned_data["postal_code"]
        city = self.cleaned_data["city"]
        country = self.cleaned_data["country"]
        if commit:
            self.user.personal.address.label_first = label_first
            self.user.personal.address.label_second = label_second
            self.user.personal.address.postal_code = postal_code
            self.user.personal.address.city = city
            self.user.personal.address.country = country
            self.user.personal.address.save()
        return self.user.personal.address


class ConfidentialityForm(ModelForm):

    class Meta:
        model = Personal
        fields = ['has_private_profile']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ConfidentialityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-update-confidentiality-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-12'
        self.helper.field_class = 'col-12'
        if self.user.personal.has_private_profile:
            self.helper.layout = Layout(Field(
                'has_private_profile',
                checked=""
            ))

    def save(self, commit=True):
        has_private_profile = self.cleaned_data["has_private_profile"]
        if commit:
            self.user.personal.has_private_profile = has_private_profile
            self.user.personal.save()
        return self.user.personal


class AddMedicalFileForm(ModelForm):

    class Meta:
        model = Personal
        fields = ['medical_file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddMedicalFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-add-medical-file-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field(
                'medical_file',
                accept=".pdf, image/png, image/jpeg",
            ),
        )
        self.helper.add_input(Submit('submit', 'Soumettre'))
        if self.is_valid():
            self.save()

    def save(self, commit=True):
        medical_file = self.cleaned_data["medical_file"]
        if commit and medical_file:
            self.user.personal.medical_file = medical_file
            self.user.personal.save()
        return self.user.personal


class AddIdFileForm(ModelForm):

    class Meta:
        model = Personal
        fields = ['id_file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddIdFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-add-id-file-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field(
                'id_file',
                accept=".pdf, image/png, image/jpeg",
            ),
        )
        self.helper.add_input(Submit('submit', 'Soumettre'))
        if self.is_valid():
            self.save()

    def save(self, commit=True):
        id_file = self.cleaned_data["id_file"]
        if commit and id_file:
            self.user.personal.id_file = id_file
            self.user.personal.save()
        return self.user.personal


class DropMedicalFileForm(ModelForm):

    class Meta:
        model = Personal
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(DropMedicalFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-drop-medical-file-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Confirmer'))
        if self.is_valid():
            self.save()

    def save(self, commit=True):
        if commit:
            self.user.personal.medical_file.delete()
            self.user.personal.save()
        return self.user.personal


class DropIdFileForm(ModelForm):

    class Meta:
        model = Personal
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(DropIdFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-drop-file-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Confirmer'))
        if self.is_valid():
            self.save()

    def save(self, commit=True):
        if commit:
            self.user.personal.id_file.delete()
            self.user.personal.save()
        return self.user.personal
