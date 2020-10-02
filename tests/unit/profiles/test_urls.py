"""Contain the unit tests related to the urls in app ``profiles``."""

from django.test import TestCase
from django.urls import reverse


class ProfilesUrlsTestCase(TestCase):
    """Test the urls in the app ``profiles``."""

    def test_profile_url(self):
        """Unit test - app ``profiles`` - url ``profile/``

        Test the profile url.
        """
        url = reverse('profiles:profile')
        self.assertEqual(url, '/profile/')

    def test_custom_password_change_url(self):
        """Unit test - app ``profiles`` - url ``profile/change_password/``

        Test the custom password change url.
        """
        url = reverse('profiles:change_password')
        self.assertEqual(url, '/profile/change_password/')

    def test_password_changed_url(self):
        """Unit test - app ``profiles`` - url ``profile/change_password/done/``

        Test the 'password changed' (confirmation) url.
        """
        url = reverse('profiles:change_password_done')
        self.assertEqual(url, '/profile/change_password/done/')

    def test_password_reset_url(self):
        """Unit test - app ``profiles`` - url ``profile/reset_password/``

        Test the password reset url.
        """
        url = reverse('profiles:reset_password')
        self.assertEqual(url, '/profile/reset_password/')

    def test_password_reset_done_url(self):
        """Unit test - app ``profiles`` - url ``profile/reset_password/done/``

        Test the 'password reset (done)' url.
        """
        url = reverse('profiles:reset_password_done')
        self.assertEqual(url, '/profile/reset_password/done/')

    def test_password_reset_confirm_url(self):
        """Unit test - app ``profiles`` - url ``profile/...``

        [complete url: ``profile/reset_password_confirm/<uidb64>/<token>/``]
        Test the 'password reset confirm' url.
        """
        url = reverse(
            'profiles:reset_password_confirm',
            kwargs={'uidb64': 'uidb64', 'token': 'token'}
        )
        self.assertEqual(
            url,
            '/profile/reset_password_confirm/uidb64/token/'
        )

    def test_password_reset_complete_url(self):
        """Unit test - app ``profiles`` - url ``profile/...``

        [complete url: ``profile/reset_password_complete/``]
        Test the 'password reset (complete)' url.
        """
        url = reverse('profiles:reset_password_complete')
        self.assertEqual(url, '/profile/reset_password_complete/')

    def test_personal_info_update_url(self):
        """Unit test - app ``profiles`` - url ``profile/update_personal_info/``

        Test the 'personal info update' url.
        """
        url = reverse('profiles:update_personal_info')
        self.assertEqual(url, '/profile/update_personal_info/')

    def test_phone_address_url(self):
        """Unit test - app ``profiles`` - url ``profile/update_phone_address/``

        Test the 'phone and address update' url.
        """
        url = reverse('profiles:update_phone_address')
        self.assertEqual(url, '/profile/update_phone_address/')

    def test_add_medical_file_url(self):
        """Unit test - app ``profiles`` - url ``profile/add_medical_file/``

        Test the 'medical file add' url.
        """
        url = reverse('profiles:add_medical_file')
        self.assertEqual(url, '/profile/add_medical_file/')

    def test_add_id_file_url(self):
        """Unit test - app ``profiles`` - url ``profile/add_id_file/``

        Test the 'id file add' url.
        """
        url = reverse('profiles:add_id_file')
        self.assertEqual(url, '/profile/add_id_file/')

    def test_drop_medical_file_url(self):
        """Unit test - app ``profiles`` - url ``profile/drop_medical_file/``

        Test the 'drop medical file' url.
        """
        url = reverse('profiles:drop_medical_file')
        self.assertEqual(url, '/profile/drop_medical_file/')

    def test_drop_id_file_url(self):
        """Unit test - app ``profiles`` - url ``profile/drop_id_file/``

        Test the 'drop id file' url.
        """
        url = reverse('profiles:drop_id_file')
        self.assertEqual(url, '/profile/drop_id_file/')

    def test_drop_file_url(self):
        """Unit test - app ``profiles`` - url ``profile/drop_file/``

        Test the 'drop file' url.
        """
        url = reverse('profiles:drop_file')
        self.assertEqual(url, '/profile/drop_file/')
