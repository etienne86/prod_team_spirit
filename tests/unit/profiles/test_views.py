"""Contain the unit tests related to the views in app ``profiles``."""

from django.http.request import HttpRequest
from django.test import TestCase

from teamspirit.core.models import Address
from teamspirit.profiles.models import Personal
from teamspirit.profiles.views import (
    add_id_file_view,
    add_medical_file_view,
    custom_password_reset_complete_view,
    custom_password_reset_done_view,
    drop_file_view,
    drop_id_file_view,
    drop_medical_file_view,
    password_changed_view,
    personal_info_view,
    phone_address_view,
    profile_view,
)
from teamspirit.users.models import User


class ProfilesViewsTestCase(TestCase):
    """Test the views in the app ``profiles``."""

    def setUp(self):
        super().setUp()
        # a user in database
        self.address = Address.objects.create(
            label_first="1 rue de l'impasse",
            label_second="",
            postal_code="75000",
            city="Paris",
            country="France"
        )
        self.personal = Personal.objects.create(
            phone_number="01 02 03 04 05",
            address=self.address
        )
        self.user = User.objects.create_user(
            email="toto@mail.com",
            first_name="Toto",
            password="TopSecret",
            personal=self.personal
        )
        # log this user in
        self.client.login(email="toto@mail.com", password="TopSecret")
        # a 'get' request
        self.get_request = HttpRequest()
        self.get_request.method = 'get'
        self.get_request.user = self.user
        # a 'post' request
        self.post_request = HttpRequest()
        self.post_request.method = 'post'
        self.post_request.user = self.user

    def test_profile_view(self):
        """Unit test - app ``profiles`` - view ``profile_view``

        Test the profile view.
        """
        view = profile_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Team Spirit - Profil</title>', html)

    # next test: status 403 (Forbidden), problem with CSRF?

    # def test_custom_password_change_view(self):
    #     """Unit test - app ``profiles`` - view ...

    #     [complete view: ``custom_password_change_view``]
    #     Test the custom password change view.
    #     """
    #     view = custom_password_change_view
    #     view = requires_csrf_token(view)
    #     response = view(self.get_request)
    #     print(response)
    #     print(type(response))
    #     # response = csrf_exempt(view)(self.get_request)
    #     # render the response content
    #     # response.render()
    #     html = response.content.decode('utf8')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(html.startswith('<!DOCTYPE html>'))
    #     self.assertIn(
    #         '<title>Team Spirit - Changement de mot de passe</title>',
    #         html
    #     )

    def test_password_changed_view(self):
        """Unit test - app ``profiles`` - view ``password_changed_view``

        Test the 'password changed' (confirmation) view.
        """
        view = password_changed_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Team Spirit - Mot de passe changé</title>', html)

    # next test: status 403 (Forbidden), problem with CSRF?

    # def test_password_reset_view(self):
    #     """Unit test - app ``profiles`` - view ``custom_password_reset_view``

    #     Test the custom password reset view.
    #     """
    #     view = custom_password_reset_view
    #     response = view(self.get_request)
    #     # response = csrf_exempt(view)(self.get_request)
    #     # render the response content
    #     # response.render()
    #     html = response.content.decode('utf8')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(html.startswith('<!DOCTYPE html>'))
    #     self.assertIn(
    #         '<title>Team Spirit - Réinitialisation du mot de passe</title>',
    #         html
    #     )

    def test_password_reset_done_view(self):
        """Unit test - app ``profiles`` - view ...

        [complete view: ``custom_password_reset_done_view``]
        Test the custom password reset (done) view.
        """
        view = custom_password_reset_done_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - '
            'Envoi d\'un mail pour réinitialisation du mot de passe</title>',
            html
        )

    # next test: AttributeError: 'NoneType' object has no attribute 'is_bound'
    # I do not know how to generate/mock the `uidb64` and `token`.

    # def test_password_reset_confirm_view(self):
    #     """Unit test - app ``profiles`` - view ...

    #     [complete view: ``custom_password_reset_confirm_view``]
    #     Test the custom password reset confirm view.
    #     """
    #     view = custom_password_reset_confirm_view
    #     response = view(self.get_request, uidb64='uidb64', token='token')
    #     print(type(response))
    #     print(response)
    #     # response = csrf_exempt(view)(self.get_request)
    #     # render the response content
    #     response.render()
    #     html = response.content.decode('utf8')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(html.startswith('<!DOCTYPE html>'))
        # self.assertIn(
        #     '<title>Team Spirit - '
        #     'Définition du nouveau mot de passe</title>',
        #     html
        # )

    def test_password_reset_complete_view(self):
        """Unit test - app ``profiles`` - view ...

        [complete view: ``custom_password_reset_complete_view``]
        Test the custom password reset (complete) view.
        """
        view = custom_password_reset_complete_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Team Spirit - Mot de passe réinitialisé', html)

    def test_personal_info_view(self):
        """Unit test - app ``profiles`` - view ``personal_info_view``

        Test the personal info view.
        """
        view = personal_info_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - Mise à jour des informations personnelles',
            html
        )

    def test_update_phone_address_view(self):
        """Unit test - app ``profiles`` - view ``phone_address_view``

        Test the phone and address view.
        """
        view = phone_address_view
        response = view(self.get_request)  # type is TemplateResponse
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - Mise à jour des coordonnées',
            html
        )

    def test_add_medical_file_view(self):
        """Unit test - app ``profiles`` - view ``add_medical_file_view``

        Test the 'medical file add' view.
        """
        view = add_medical_file_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - Mise à jour du certificat médical ou de la'
            ' licence',
            html
        )

    def test_add_id_file_view(self):
        """Unit test - app ``profiles`` - view ``add_id_file_view``

        Test the 'id file add' view.
        """
        view = add_id_file_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - Mise à jour de la pièce d\'identité',
            html
        )

    def test_drop_medical_file_view(self):
        """Unit test - app ``profiles`` - view ``drop_medical_file_view``

        Test the 'medical file drop' view.
        """
        view = drop_medical_file_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - Suppression du certificat médical ou de la'
            ' licence',
            html
        )

    def test_drop_id_file_view(self):
        """Unit test - app ``profiles`` - view ``drop_id_file_view``

        Test the 'id file drop' view.
        """
        view = drop_id_file_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - Suppression de la pièce d\'identité',
            html
        )

    def test_drop_file_view(self):
        """Unit test - app ``profiles`` - view ``drop_file_view``

        Test the 'file drop' view.
        """
        view = drop_file_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - Suppression d\'un fichier',
            html
        )
