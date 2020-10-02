"""Contain the unit tests related to the models in app ``profiles``."""


from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase

from teamspirit.core.models import Address
from teamspirit.profiles.models import Personal, Role


class PersonalModelTestsCase(TestCase):
    """Test the model ``Personal``."""

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
        cls.id_file = UploadedFile()
        cls.medical_file = UploadedFile()
        cls.personal_public = Personal.objects.create(
            phone_number="01 02 03 04 05",
            address=cls.address,
            id_file=cls.id_file,
            medical_file=cls.medical_file
        )
        cls.personal_private = Personal.objects.create(
            phone_number="05 04 03 02 01",
            address=cls.address,
            id_file=cls.id_file,
            medical_file=cls.medical_file,
            has_private_profile=True
        )

    def test_personal_is_personal_instance(self):
        """Unit test - app ``profiles`` - model ``Personal`` - #1.1

        Test that personal is a ``Personal`` instance.
        """
        self.assertIsInstance(self.personal_public, Personal)

    def test_phone_number(self):
        """Unit test - app ``profiles`` - model ``Personal`` - #1.2

        Test the phone number.
        """
        self.assertIsInstance(self.personal_public.phone_number, str)
        self.assertEqual(self.personal_public.phone_number, "01 02 03 04 05")

    def test_address(self):
        """Unit test - app ``profiles`` - model ``Personal`` - #1.3

        Test the address.
        """
        self.assertIsInstance(self.personal_public.address, Address)
        self.assertEqual(self.personal_public.address, self.address)

    def test_has_not_private_profile(self):
        """Unit test - app ``profiles`` - model ``Personal`` - #1.4

        Test the non-private (i.e. public) profile.
        """
        self.assertIsInstance(self.personal_public.has_private_profile, bool)
        self.assertFalse(self.personal_public.has_private_profile)

    def test_has_private_profile(self):
        """Unit test - app ``profiles`` - model ``Personal`` - #1.5

        Test the private profile.
        """
        self.assertIsInstance(self.personal_private.has_private_profile, bool)
        self.assertTrue(self.personal_private.has_private_profile)

    def test_id_file(self):
        """Unit test - app ``profiles`` - model ``Personal`` - #1.6

        Test the id_file.
        """
        self.assertIsInstance(self.personal_public.id_file, File)
        self.assertEqual(self.personal_public.id_file, self.id_file)

    def test_medical_file(self):
        """Unit test - app ``profiles`` - model ``Personal`` - #1.7

        Test the medical_file.
        """
        self.assertIsInstance(self.personal_public.medical_file, File)
        self.assertEqual(self.personal_public.medical_file, self.medical_file)


class RoleModelTestCase(TestCase):
    """Test the model ``Role``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.member = Role.objects.create()
        cls.secretary = Role.objects.create()
        cls.secretary.set_as_secretary()
        cls.treasurer = Role.objects.create()
        cls.treasurer.set_as_treasurer()
        cls.president = Role.objects.create()
        cls.president.set_as_president()
        cls.inactive = Role.objects.create()
        cls.inactive.set_as_inactive()

    def test_member_is_role_instance(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.1

        Test that member is a ``Role`` instance.
        """
        self.assertIsInstance(self.member, Role)
        self.assertIsInstance(self.member.is_member, bool)

    def test_member_is_member(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.2

        Test that the member is member.
        """
        self.assertTrue(self.member.is_member)

    def test_member_is_not_secretary(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.3

        Test that the member is not secretary.
        """
        self.assertFalse(self.member.is_secretary)

    def test_member_is_not_treasurer(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.4

        Test that the member is not treasurer.
        """
        self.assertFalse(self.member.is_treasurer)

    def test_member_is_not_president(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.5

        Test that the member is not president.
        """
        self.assertFalse(self.member.is_president)

    def test_member_is_not_inactive(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.6

        Test that the member is not inactive.
        """
        self.assertFalse(self.member.is_inactive)

    def test_secretary_is_role_instance(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.7

        Test that secretary is a ``Role`` instance.
        """
        self.assertIsInstance(self.secretary, Role)
        self.assertIsInstance(self.secretary.is_secretary, bool)

    def test_secretary_is_secretary(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.8

        Test that the secreatary is secretary.
        """
        self.assertTrue(self.secretary.is_secretary)

    def test_secretary_is_not_member(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.9

        Test that the secretary is not member.
        """
        self.assertFalse(self.secretary.is_member)

    def test_secretary_is_not_treasurer(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.10

        Test that the secretary is not treasurer.
        """
        self.assertFalse(self.secretary.is_treasurer)

    def test_secretary_is_not_president(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.11

        Test that the secretary is not president.
        """
        self.assertFalse(self.secretary.is_president)

    def test_secretary_is_not_inactive(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.12

        Test that the secretary is not inactive.
        """
        self.assertFalse(self.secretary.is_inactive)

    def test_treasurer_is_role_instance(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.13

        Test that treasurer is a ``Role`` instance.
        """
        self.assertIsInstance(self.treasurer, Role)
        self.assertIsInstance(self.treasurer.is_treasurer, bool)

    def test_treasurer_is_treasurer(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.14

        Test that the treasurer is treasurer.
        """
        self.assertTrue(self.treasurer.is_treasurer)

    def test_treasurer_is_not_member(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.15

        Test that the treasurer is not member.
        """
        self.assertFalse(self.treasurer.is_member)

    def test_treasurer_is_not_secretary(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.16

        Test that the treasurer is not secretary.
        """
        self.assertFalse(self.treasurer.is_secretary)

    def test_treasurer_is_not_president(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.17

        Test that the treasurer is not president.
        """
        self.assertFalse(self.treasurer.is_president)

    def test_treasurer_is_not_inactive(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.18

        Test that the treasurer is not inactive.
        """
        self.assertFalse(self.treasurer.is_inactive)

    def test_president_is_role_instance(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.19

        Test that president is a ``Role`` instance.
        """
        self.assertIsInstance(self.president, Role)
        self.assertIsInstance(self.president.is_president, bool)

    def test_president_is_president(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.20

        Test that the president is president.
        """
        self.assertTrue(self.president.is_president)

    def test_president_is_not_member(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.21

        Test that the president is not member.
        """
        self.assertFalse(self.president.is_member)

    def test_president_is_not_secretary(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.22

        Test that the president is not secretary.
        """
        self.assertFalse(self.president.is_secretary)

    def test_president_is_not_treasurer(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.23

        Test that the president is not treasurer.
        """
        self.assertFalse(self.president.is_treasurer)

    def test_president_is_not_inactive(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.24

        Test that the president is not inactive.
        """
        self.assertFalse(self.president.is_inactive)

    def test_inactive_is_role_instance(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.25

        Test that inactive is a ``Role`` instance.
        """
        self.assertIsInstance(self.inactive, Role)
        self.assertIsInstance(self.inactive.is_inactive, bool)

    def test_inactive_is_inactive(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.26

        Test that the inactive is inactive.
        """
        self.assertTrue(self.inactive.is_inactive)

    def test_inactive_is_not_member(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.27

        Test that the inactive is not member.
        """
        self.assertFalse(self.inactive.is_member)

    def test_inactive_is_not_secretary(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.28

        Test that the inactive is not secretary.
        """
        self.assertFalse(self.inactive.is_secretary)

    def test_inactive_is_not_treasurer(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.29

        Test that the inactive is not treasurer.
        """
        self.assertFalse(self.inactive.is_treasurer)

    def test_inactive_is_not_president(self):
        """Unit test - app ``profiles`` - model ``Role`` - #2.30

        Test that the inactive is not president.
        """
        self.assertFalse(self.inactive.is_president)
