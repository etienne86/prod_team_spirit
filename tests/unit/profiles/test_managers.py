"""
This module contains the unit tests related to
the managers in app ``profiles``.
"""

from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase

from teamspirit.core.models import Address
from teamspirit.profiles.managers import rename_id_file, rename_medical_file
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class ProfilesManagersTestCase(TestCase):
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
            id_file=UploadedFile(),
            medical_file=UploadedFile(),
            address=self.address
        )
        self.user = User.objects.create_user(
            email="toto@mail.com",
            first_name="Toto",
            last_name="LE RIGOLO",
            password="TopSecret",
            personal=self.personal
        )
        # log this user in
        self.client.login(email="toto@mail.com", password="TopSecret")

    def test_rename_id_file(self):
        instance = self.user.personal
        file_name = self.user.personal.id_file.name
        renamed_filed = rename_id_file(instance, file_name)
        expected_renaming = "id/LE RIGOLO_Toto/None"
        self.assertEqual(renamed_filed, expected_renaming)

    def test_rename_medical_file(self):
        instance = self.user.personal
        file_name = self.user.personal.medical_file.name
        renamed_filed = rename_medical_file(instance, file_name)
        expected_renaming = "lic/LE RIGOLO_Toto/None"
        self.assertEqual(renamed_filed, expected_renaming)
