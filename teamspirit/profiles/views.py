from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from teamspirit.profiles.forms import (
    AddIdFileForm,
    AddMedicalFileForm,
    AddressForm,
    ConfidentialityForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    DropIdFileForm,
    DropMedicalFileForm,
    PersonalInfoForm,
    PhoneForm,
)


class ProfileView(TemplateView):

    template_name = "profiles/profile.html"


profile_view = ProfileView.as_view()
profile_view = login_required(profile_view)


class CustomPasswordChangeView(PasswordChangeView):

    template_name = 'profiles/change_password.html'
    success_url = 'done'
    form_class = CustomPasswordChangeForm


custom_password_change_view = CustomPasswordChangeView.as_view()
custom_password_change_view = login_required(custom_password_change_view)


class PasswordChangedView(TemplateView):

    template_name = 'profiles/password_changed.html'


password_changed_view = PasswordChangedView.as_view()
password_changed_view = login_required(password_changed_view)


class CustomPasswordResetView(PasswordResetView):

    template_name = 'profiles/reset_password/password_reset.html'
    form_class = CustomPasswordResetForm
    subject_template_name = 'profiles/reset_password/' \
        'password_reset_subject.txt'
    email_template_name = 'profiles/reset_password/password_reset_email.html'
    success_url = 'done'


custom_password_reset_view = CustomPasswordResetView.as_view()


class CustomPasswordResetDoneView(PasswordResetDoneView):

    template_name = 'profiles/reset_password/password_reset_done.html'


custom_password_reset_done_view = CustomPasswordResetDoneView.as_view()


class CustomPasswordResetConfirmView(PasswordResetConfirmView):

    template_name = 'profiles/reset_password/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('profiles:reset_password_complete')


custom_password_reset_confirm_view = CustomPasswordResetConfirmView.as_view()


class CustomPasswordResetCompleteView(PasswordResetCompleteView):

    template_name = 'profiles/reset_password/password_reset_complete.html'


custom_password_reset_complete_view = CustomPasswordResetCompleteView.as_view()


class PersonalInfoView(FormView):

    template_name = 'profiles/update_personal_info.html'
    form_class = PersonalInfoForm
    success_url = reverse_lazy('profiles:profile')

    def get_form_kwargs(self):
        kwargs = super(PersonalInfoView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


personal_info_view = PersonalInfoView.as_view()
personal_info_view = login_required(personal_info_view)


@login_required
def phone_address_view(request):
    context = {}
    if request.method == 'POST':
        phone_form = PhoneForm(request.POST, user=request.user)
        address_form = AddressForm(request.POST, user=request.user)
        confidentiality_form = ConfidentialityForm(
            request.POST,
            user=request.user
        )
        if all([
            phone_form.is_valid(),
            address_form.is_valid(),
            confidentiality_form.is_valid()
        ]):
            # process forms
            phone_form.save()
            address_form.save()
            confidentiality_form.save()
            # redirect to the profile url
            return redirect(reverse_lazy('profiles:profile'))
    else:
        phone_form = PhoneForm(user=request.user)
        address_form = AddressForm(user=request.user)
        confidentiality_form = ConfidentialityForm(user=request.user)
    context['phone_form'] = phone_form
    context['address_form'] = address_form
    context['confidentiality_form'] = confidentiality_form
    return render(
        request,
        'profiles/update_phone_address.html',
        context,
    )


class AddMedicalFileView(FormView):

    template_name = 'profiles/add_medical_file.html'
    form_class = AddMedicalFileForm
    success_url = reverse_lazy('profiles:profile')

    def get_form_kwargs(self):
        kwargs = super(AddMedicalFileView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


add_medical_file_view = AddMedicalFileView.as_view()
add_medical_file_view = login_required(add_medical_file_view)


class AddIdFileView(FormView):

    template_name = 'profiles/add_id_file.html'
    form_class = AddIdFileForm
    success_url = reverse_lazy('profiles:profile')

    def get_form_kwargs(self):
        kwargs = super(AddIdFileView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


add_id_file_view = AddIdFileView.as_view()
add_id_file_view = login_required(add_id_file_view)


class DropMedicalFileView(FormView):

    template_name = 'profiles/drop_medical_file.html'
    form_class = DropMedicalFileForm
    success_url = reverse_lazy('profiles:drop_file')

    def get_form_kwargs(self):
        kwargs = super(DropMedicalFileView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


drop_medical_file_view = DropMedicalFileView.as_view()
drop_medical_file_view = login_required(drop_medical_file_view)


class DropIdFileView(FormView):

    template_name = 'profiles/drop_id_file.html'
    form_class = DropIdFileForm
    success_url = reverse_lazy('profiles:drop_file')

    def get_form_kwargs(self):
        kwargs = super(DropIdFileView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


drop_id_file_view = DropIdFileView.as_view()
drop_id_file_view = login_required(drop_id_file_view)


class DropFileView(TemplateView):

    template_name = 'profiles/drop_file.html'


drop_file_view = DropFileView.as_view()
drop_file_view = login_required(drop_file_view)
