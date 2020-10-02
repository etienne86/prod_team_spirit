"""Contain the unit tests related to the models in app ``catalogs``."""

from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase

from teamspirit.catalogs.models import Catalog, Product


class CatalogModelTestsCase(TestCase):
    """Test the model ``Catalog``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.catalog = Catalog.objects.create(
            name="Catalogue de vêtements",
        )

    def test_catalog_is_catalog_instance(self):
        """Unit test - app ``catalogs`` - model ``Product`` - #1.1

        Test that catalog is a ``Catalog`` instance.
        """
        self.assertIsInstance(self.catalog, Catalog)

    def test_name(self):
        """Unit test - app ``catalogs`` - model ``Catalog`` - #1.2

        Test the name.
        """
        self.assertIsInstance(self.catalog.name, str)
        self.assertEqual(self.catalog.name, "Catalogue de vêtements")


class ProductModelTestsCase(TestCase):
    """Test the model ``Product``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.catalog = Catalog.objects.create(
            name="Catalogue de vêtements",
        )
        cls.image = UploadedFile()
        cls.product = Product.objects.create(
            name="Débardeur homme",
            image=cls.image,
            is_available=True,
            is_free=False,
            price=25,
            catalog=cls.catalog,
        )

    def test_product_is_product_instance(self):
        """Unit test - app ``catalogs`` - model ``Product`` - #2.1

        Test that product is a ``Product`` instance.
        """
        self.assertIsInstance(self.product, Product)

    def test_name(self):
        """Unit test - app ``catalogs`` - model ``Product`` - #2.2

        Test the name.
        """
        self.assertIsInstance(self.product.name, str)
        self.assertEqual(self.product.name, "Débardeur homme")

    def test_image(self):
        """Unit test - app ``catalogs`` - model ``Product`` - #2.3

        Test the image.
        """
        self.assertIsInstance(self.product.image, File)
        self.assertEqual(self.product.image, self.image)

    def test_is_available(self):
        """Unit test - app ``catalogs`` - model ``Product`` - #2.4

        Test the availability.
        """
        self.assertIsInstance(self.product.is_available, bool)
        self.assertEqual(self.product.is_available, True)

    def test_is_free(self):
        """Unit test - app ``catalogs`` - model ``Product`` - #2.5

        Test wether the item is free.
        """
        self.assertIsInstance(self.product.is_free, bool)
        self.assertEqual(self.product.is_free, False)

    def test_price(self):
        """Unit test - app ``catalogs`` - model ``Product`` - #2.6

        Test the price.
        """
        self.assertIsInstance(self.product.price, int)
        self.assertEqual(self.product.price, 25)

    def test_catalog(self):
        """Unit test - app ``catalogs`` - model ``Product`` - #2.7

        Test the catalog.
        """
        self.assertIsInstance(self.product.catalog, Catalog)
        self.assertEqual(self.product.catalog, self.catalog)
