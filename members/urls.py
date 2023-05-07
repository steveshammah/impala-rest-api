from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path(
        "login/",
        views.AuthViewSet.as_view({"post": "login"}),
    ),
    path(
        "retrieve/",
        views.AuthViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
    path(
        "logout/",
        views.AuthViewSet.as_view(
            {
                "post": "logout",
            }
        ),
    ),
]