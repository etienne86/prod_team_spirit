"""Contain the unit tests related to the models in app ``core``."""

from django.test import TestCase

from teamspirit.core.models import Address, Location


class AddressModelTestsCase(TestCase):
    """Test the model ``Address``."""

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

    def test_address_is_address_instance(self):
        """Unit test - app ``core`` - model ``Address`` - #1.1

        Test that address is an ``Address`` instance.
        """
        self.assertIsInstance(self.address, Address)

    def test_label_first(self):
        """Unit test - app ``core`` - model ``Address`` - #1.2

        Test the label (first line).
        """
        self.assertIsInstance(self.address.label_first, str)
        self.assertEqual(self.address.label_first, "1 rue de l'impasse")

    def test_label_seconde(self):
        """Unit test - app ``core`` - model ``Address`` - #1.3

        Test the label (second line).
        """
        self.assertIsInstance(self.address.label_second, str)
        self.assertEqual(self.address.label_second, "")

    def test_postal_code(self):
        """Unit test - app ``core`` - model ``Address`` - #1.4

        Test the postal code.
        """
        self.assertIsInstance(self.address.postal_code, str)
        self.assertEqual(self.address.postal_code, "75000")

    def test_city(self):
        """Unit test - app ``core`` - model ``Address`` - #1.5

        Test the city.
        """
        self.assertIsInstance(self.address.city, str)
        self.assertEqual(self.address.city, "Paris")

    def test_country(self):
        """Unit test - app ``core`` - model ``Address`` - #1.6

        Test the country.
        """
        self.assertIsInstance(self.address.country, str)
        self.assertEqual(self.address.country, "France")


class LocationModelTestsCase(TestCase):
    """Test the model ``Location``."""

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
        cls.location = Location.objects.create(
            name="Chez Toto",
            address=cls.address
        )

    def test_location_is_location_instance(self):
        """Unit test - app ``core`` - model ``Location`` - #2.1

        Test that location is a location.
        """
        self.assertIsInstance(self.location, Location)

    def test_location_name(self):
        """Unit test - app ``core`` - model ``Location`` - #2.2

        Test the location name.
        """
        self.assertIsInstance(self.location.name, str)
        self.assertEqual(self.location.name, "Chez Toto")

    def test_location_address(self):
        """Unit test - app ``core`` - model ``Location`` - #2.3

        Test the location address.
        """
        self.assertIsInstance(self.location.address, Address)
        self.assertEqual(self.location.address, self.address)
