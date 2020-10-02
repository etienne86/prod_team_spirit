"""Contain the managers for the models in app ``catalogs``."""

from django.db import models


class CatalogManager(models.Manager):
    """Manage the model ``Catalog``."""
    pass


class ProductManager(models.Manager):
    """Manage the model ``Product``."""
    pass
