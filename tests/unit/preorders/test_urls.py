"""
This module contains the unit tests related to
the urls in app ``preorders``.
"""

from django.test import TestCase
from django.urls import reverse


class PreordersUrlsTestCase(TestCase):
    """Test the urls in the app ``preorders``."""

    def test_shopping_cart_url(self):
        """Unit test - app ``preorders`` - url ``shopping_cart/``

        Test the shopping cart url.
        """
        url = reverse('preorders:shopping_cart')
        self.assertEqual(url, '/shopping_cart/')

    def test_add_to_cart_url(self):
        """Unit test - app ``preorders`` - url ``shopping_cart/...``

        [complete url: ``shopping_cart/add_product/<product_id>/``]
        Test the 'add to cart' url.
        """
        url = reverse('preorders:add_to_cart', kwargs={'product_id': 1})
        self.assertEqual(url, '/shopping_cart/add_product/1/')

    def test_drop_from_cart_url(self):
        """Unit test - app ``preorders`` - url ``shopping_cart/drop_product/``

        Test the 'drop from cart' url.
        """
        url = reverse('preorders:drop_from_cart', kwargs={'line_id': 1})
        self.assertEqual(url, '/shopping_cart/drop_product/1/')
