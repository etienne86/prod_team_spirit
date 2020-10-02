"""
This module contains the unit tests related to
the views in app ``preorders``.
"""

from django.core.files.uploadedfile import UploadedFile
from django.http.request import HttpRequest
from django.test import TestCase

from teamspirit.catalogs.models import Catalog, Product
from teamspirit.core.models import Address
from teamspirit.preorders.models import ShoppingCart, ShoppingCartLine
from teamspirit.preorders.views import (
    add_to_cart_view,
    drop_from_cart_view,
    shopping_cart_view,
)
from teamspirit.profiles.models import Personal
from teamspirit.users.models import User


class PreordersViewsTestCase(TestCase):
    """Test the views in the app ``preorders``."""

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
        # some other data
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
        self.shopping_cart = ShoppingCart.objects.create(
            user=self.user,
        )
        self.shopping_cart_line = ShoppingCartLine.objects.create(
            shopping_cart=self.shopping_cart,
            product=self.product,
            quantity=1,
            size='M',
        )

    def test_shopping_cart_view(self):
        """Unit test - app ``preorders`` - view ``shopping_cart_view``

        Test the shopping cart view.
        """
        view = shopping_cart_view
        response = view(self.get_request)  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - Panier de pré-commande</title>',
            html
        )

    def test_add_to_cart_view(self):
        """Unit test - app ``preorders`` - view ``add_to_cart_view``

        Test the 'add to cart' view.
        """
        view = add_to_cart_view
        response = view(
            self.get_request,
            product_id=self.product.id
        )  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Team Spirit - Ajout de produit</title>', html)

    def test_drop_from_cart_view(self):
        """Unit test - app ``preorders`` - view ``drop_from_cart_view``

        Test the 'drop from cart' view.
        """
        view = drop_from_cart_view
        response = view(
            self.get_request,
            line_id=self.shopping_cart_line.id
        )  # type is TemplateResponse
        # render the response content
        response.render()
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn(
            '<title>Team Spirit - Suppression de produit</title>',
            html
        )
