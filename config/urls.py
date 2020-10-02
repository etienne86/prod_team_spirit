from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

from teamspirit.core.views import contact_view, home_view, legal_view

urlpatterns = [
    path("", home_view, name="home"),
    path("contact/", contact_view, name="contact"),
    path("legal/", legal_view, name="legal"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("teamspirit.users.urls")),
    # path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("catalog/", include("teamspirit.catalogs.urls")),
    path("events/", include("teamspirit.events.urls")),
    path("shopping_cart/", include("teamspirit.preorders.urls")),
    path("profile/", include("teamspirit.profiles.urls")),
    path("trainings/", include("teamspirit.trainings.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls))
        ] + urlpatterns
