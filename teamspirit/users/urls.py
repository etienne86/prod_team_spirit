from django.urls import path

from teamspirit.users.views import (
    custom_login_view,
    custom_logout_view,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("login/", custom_login_view, name="login"),
    path("logout/", custom_logout_view, name="logout"),
    path("~redirect/", user_redirect_view, name="redirect"),
    path("~update/", user_update_view, name="update"),
    path("<str:email>/", user_detail_view, name="detail"),
]
