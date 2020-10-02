"""Contain the unit tests related to the forms in app ``preorders``."""

from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase

from teamspirit.catalogs.models import Catalog, Product
from teamspirit.core.models import Address
from teamspirit.preorders.forms import AddToCartForm, DropFromCartForm
from teamspirit.preorders.models import ShoppingCart, ShoppingCartLine
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class PreordersFormsTestCase(TestCase):
    """Test the forms in the app ``preorders``."""

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
            password="Password123",
            first_name="Toto",
            last_name="LE RIGOLO",
            personal=self.personal
        )
        # log this user in
        self.client.login(email="toto@mail.com", password="Password123")
        # some other data
        self.shopping_cart = ShoppingCart.objects.create(
            user=self.user,
        )
        self.catalog = Catalog.objects.create(
            name="Catalogue de vêtements",
        )
        self.image = UploadedFile()
        self.product = Product.objects.create(
            name="Débardeur homme",
            image=self.image,
            is_available=True,
            is_free=False,
            price=25,
            catalog=self.catalog,
        )
        self.shopping_cart_line = ShoppingCartLine.objects.create(
            shopping_cart=self.shopping_cart,
            product=self.product,
            quantity=2,
            size='XS'
        )

    def test_add_to_cart_form_success(self):
        """Unit test - app ``preorders`` - form ``AddToCartForm``

        Test the 'product add to cart' form with success.
        """
        # count the records in database: before
        records_before = ShoppingCartLine.objects.all().count()
        # process the form
        form_data = {
            'shopping_cart': self.shopping_cart,
            'product': self.product,
            'quantity': 1,
            'size': 'M',
        }
        form = AddToCartForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        expected_shopping_cart_line = ShoppingCartLine(
            shopping_cart=self.shopping_cart,
            product=self.product,
            quantity=1,
            size='M'
        )
        # count the records in database: after
        records_after = ShoppingCartLine.objects.all().count()
        # is one record added in database?
        self.assertEqual(records_after, records_before + 1)
        # is this last record as expected?
        last_record = ShoppingCartLine.objects.all()[records_after - 1]
        self.assertEqual(
            last_record.shopping_cart,
            expected_shopping_cart_line.shopping_cart
        )
        self.assertEqual(
            last_record.product,
            expected_shopping_cart_line.product
        )
        self.assertEqual(
            last_record.quantity,
            expected_shopping_cart_line.quantity
        )
        self.assertEqual(
            last_record.size,
            expected_shopping_cart_line.size
        )

    def test_drop_from_cart_form_success(self):
        """Unit test - app ``preorders`` - form ``DropFromCartForm``

        Test the 'product drop from cart' form with success.
        """
        # count the records in database: before
        records_before = ShoppingCartLine.objects.all().count()
        # process the form
        form = DropFromCartForm(
            data={},
            request_user=self.user,
            line_id=self.shopping_cart_line.id,
            shopping_cart_line=self.shopping_cart_line
        )
        self.assertTrue(form.is_valid())
        # count the records in database: after
        records_after = ShoppingCartLine.objects.all().count()
        # is one record added in database?
        self.assertEqual(records_after, records_before - 1)
