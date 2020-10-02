"""Contain the unit tests related to the forms in app ``users``."""

from django import forms as django_forms
from django.test import TestCase

from teamspirit.core.models import Address
from teamspirit.profiles.models import Personal
from teamspirit.users.forms import CustomAuthenticationForm
from teamspirit.users.models import User


class UsersFormsTestCase(TestCase):
    """Test the forms in the app ``users``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address = Address.objects.create(
            label_first="1 rue de l'impasse",
            label_second="",
            postal_code="75000",
            city="Paris",
            country="France"
        )
        cls.personal = Personal.objects.create(
            phone_number="01 02 03 04 05",
            address=cls.address
        )
        cls.user = User.objects.create_user(
            email="toto@mail.com",
            password="Password123",
            first_name="Toto",
            last_name="LE RIGOLO",
            personal=cls.personal
        )
        cls.inactive_user = User.objects.create_user(
            email="titi@mail.com",
            password="Password456",
            first_name="Titi",
            last_name="LE RIKIKI",
            is_active=False,
            personal=cls.personal
        )

    def test_custom_authentication_form_success(self):
        """Unit test - app ``users`` - form ``CustomAuthenticationForm`` #1

        Test the authentication form with success.
        """
        form_data = {
            'username': 'toto@mail.com',
            'password': 'Password123'
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_authentication_form_failure_wrong_username(self):
        """Unit test - app ``users`` - form ``CustomAuthenticationForm`` #2

        Test the authentication form with a failure mode: a wrong username.
        """
        form_data = {
            'username': 'unknown@mail.com',
            'password': 'Password123'
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                '__all__':
                [
                    "Saisissez un Courriel et un mot de passe valides. "
                    "Remarquez que chacun de ces champs est sensible à la "
                    "casse (différenciation des majuscules/minuscules)."
                ]
            }
        )

    def test_custom_authentication_form_failure_wrong_password(self):
        """Unit test - app ``users`` - form ``CustomAuthenticationForm`` #3

        Test the authentication form with a failure mode: a wrong password.
        """
        form_data = {
            'username': 'toto@mail.com',
            'password': 'WrongPassword123'
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                '__all__':
                [
                    "Saisissez un Courriel et un mot de passe valides. "
                    "Remarquez que chacun de ces champs est sensible à la "
                    "casse (différenciation des majuscules/minuscules)."
                ]
            }
        )

    def test_custom_authentication_form_failure_inactive_user(self):
        """Unit test - app ``users`` - form ``CustomAuthenticationForm`` #4

        Test the authentication form with a failure mode: an inactive user.
        """
        form_data = {
            'username': 'titi@mail.com',
            'password': 'Password456'
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            expected_exception=django_forms.ValidationError,
            expected_message="Ce compte est inactif."
        )
