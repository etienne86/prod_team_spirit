from django.urls import path

from teamspirit.catalogs.views import catalog_view

app_name = 'catalogs'

urlpatterns = [
    path('', catalog_view, name="catalog"),
]
