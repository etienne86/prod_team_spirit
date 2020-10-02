"""Contain the unit tests related to the models in app ``preorders``."""

from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase

from teamspirit.catalogs.models import Catalog, Product
from teamspirit.core.models import Address
from teamspirit.preorders.models import ShoppingCart, ShoppingCartLine
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class ShoppingCartModelTestsCase(TestCase):
    """Test the model ``ShoppingCart``."""

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
        cls.toto = User.objects.create_user(
            email="toto@mail.com",
            password="Password123",
            first_name="Toto",
            last_name="LE RIGOLO",
            personal=cls.personal
        )
        cls.shopping_cart = ShoppingCart.objects.create(
            user=cls.toto,
        )
        cls.catalog = Catalog.objects.create(
            name="Catalogue de vêtements",
        )
        cls.image = UploadedFile()
        cls.product_a = Product.objects.create(
            name="Débardeur homme",
            image=cls.image,
            is_available=True,
            is_free=False,
            price=25,
            catalog=cls.catalog,
        )
        cls.product_b = Product.objects.create(
            name="T-shirt femme",
            image=cls.image,
            is_available=True,
            is_free=False,
            price=30,
            catalog=cls.catalog,
        )
        cls.shopping_cart_line_a = ShoppingCartLine.objects.create(
            shopping_cart=cls.shopping_cart,
            product=cls.product_a,
            quantity=1,
            size='M',
        )
        cls.shopping_cart_line_b = ShoppingCartLine.objects.create(
            shopping_cart=cls.shopping_cart,
            product=cls.product_b,
            quantity=2,
            size='S',
        )

    def test_shopping_cart_is_shopping_cart_instance(self):
        """Unit test - app ``preorders`` - model ``ShoppingCart`` - #1.1

        Test that a shopping cart is a ``ShoppingCart`` instance.
        """
        self.assertIsInstance(self.shopping_cart, ShoppingCart)

    def test_user(self):
        """Unit test - app ``preorders`` - model ``ShoppingCart`` - #1.2

        Test the user.
        """
        self.assertIsInstance(self.shopping_cart.user, User)
        self.assertEqual(self.shopping_cart.user, self.toto)

    def test_is_open(self):
        """Unit test - app ``preorders`` - model ``ShoppingCart`` - #1.3

        Test wether the shopping cart is open.
        """
        self.assertIsInstance(self.shopping_cart.is_open, bool)
        self.assertEqual(self.shopping_cart.is_open, True)

    def test_get_cart_amount(self):
        """Unit test - app ``preorders`` - model ``ShoppingCart`` - #1.4

        Test wether the cart amount is correct.
        """
        self.assertEqual(self.shopping_cart.get_cart_amount(), 25 + 30 * 2)


class ShoppingCartLineModelTestsCase(TestCase):
    """Test the model ``ShoppingCartLine``."""

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
        cls.toto = User.objects.create_user(
            email="toto@mail.com",
            password="Password123",
            first_name="Toto",
            last_name="LE RIGOLO",
            personal=cls.personal
        )
        cls.shopping_cart = ShoppingCart.objects.create(
            user=cls.toto,
        )
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
        cls.shopping_cart_line = ShoppingCartLine.objects.create(
            shopping_cart=cls.shopping_cart,
            product=cls.product,
            quantity=3,
            size='M',
        )

    def test_shopping_cart_line_is_shopping_cart_line_instance(self):
        """Unit test - app ``preorders`` - model ``ShoppingCartLine`` - #2.1

        Test that a shopping cart line is a ``ShoppingCartLine`` instance.
        """
        self.assertIsInstance(self.shopping_cart_line, ShoppingCartLine)

    def test_shopping_cart(self):
        """Unit test - app ``preorders`` - model ``ShoppingCartLine`` - #2.2

        Test the shopping cart.
        """
        self.assertIsInstance(
            self.shopping_cart_line.shopping_cart,
            ShoppingCart
        )
        self.assertEqual(
            self.shopping_cart_line.shopping_cart,
            self.shopping_cart
        )

    def test_product(self):
        """Unit test - app ``preorders`` - model ``ShoppingCartLine`` - #2.3

        Test the product.
        """
        self.assertIsInstance(self.shopping_cart_line.product, Product)
        self.assertEqual(self.shopping_cart_line.product, self.product)

    def test_quantity(self):
        """Unit test - app ``preorders`` - model ``ShoppingCartLine`` - #2.4

        Test the quantity.
        """
        self.assertIsInstance(self.shopping_cart_line.quantity, int)
        self.assertEqual(self.shopping_cart_line.quantity, 3)

    def test_size(self):
        """Unit test - app ``preorders`` - model ``ShoppingCartLine`` - #2.5

        Test the size.
        """
        self.assertIsInstance(self.shopping_cart_line.size, str)
        self.assertEqual(self.shopping_cart_line.size, 'M')

    def test_get_line_amount(self):
        """Unit test - app ``preorders`` - model ``ShoppingCartLine`` - #2.6

        Test wether the line amount is correct.
        """
        self.assertEqual(self.shopping_cart_line.get_line_amount(), 25 * 3)
