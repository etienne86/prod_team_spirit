from django.urls import path

from teamspirit.preorders.views import (
    add_to_cart_view,
    drop_from_cart_view,
    shopping_cart_view,
)

app_name = 'preorders'

urlpatterns = [
    path(
        '',
        shopping_cart_view,
        name='shopping_cart'
    ),
    path(
        'add_product/<int:product_id>/',
        add_to_cart_view,
        name='add_to_cart'
    ),
    path(
        'drop_product/<int:line_id>/',
        drop_from_cart_view,
        name='drop_from_cart'
    ),
]
