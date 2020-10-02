from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from teamspirit.catalogs.models import Product


class CatalogView(ListView):

    model = Product
    template_name = "catalogs/catalog.html"


catalog_view = CatalogView.as_view()
catalog_view = login_required(catalog_view)
