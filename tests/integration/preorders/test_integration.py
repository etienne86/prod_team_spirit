"""Contain the integration tests in app ``preorders``."""

from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase
from django.urls import reverse

from teamspirit.catalogs.models import Catalog, Product
from teamspirit.core.models import Address
from teamspirit.preorders.models import ShoppingCart, ShoppingCartLine
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class PreordersIntegrationTestCase(TestCase):
    """Test integration in the app ``preorders``."""

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

    def test_shopping_cart_view_with_url(self):
        """Integration test - app ``preorders`` - view with url #1

        Test the shopping cart view with url.
        """
        url = reverse('preorders:shopping_cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preorders/shopping_cart.html')

    def test_add_to_cart_view_with_url(self):
        """Integration test - app ``preorders`` - view with url #2

        Test the 'add to cart' view with url.
        """
        url = reverse(
            'preorders:add_to_cart',
            kwargs={'product_id': self.product.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preorders/add_to_cart.html')

    def test_drop_from_cart_view_with_url(self):
        """Integration test - app ``preorders`` - view with url #3

        Test the 'drop from cart' view with url.
        """
        url = reverse(
            'preorders:drop_from_cart',
            kwargs={'line_id': self.shopping_cart_line.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preorders/drop_from_cart.html')
