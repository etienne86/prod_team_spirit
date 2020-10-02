from django.contrib import admin

from teamspirit.preorders.models import ShoppingCart, ShoppingCartLine

admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartLine)
