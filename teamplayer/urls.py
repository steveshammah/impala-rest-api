from django.urls import path, re_path
from . import views

PVAR_PROFILE_ID = r"(?P<lookup_value>[\w\-\@\.\$]+)"
PVAR_TOKEN = r"(?P<token>[\w]+)"

urlpatterns = [
    re_path(
            r"^v1/teams/$",
            views.TeamViewSet.as_view(
                {
                    "get": "list",
                    "post": "create",
                }
            ),
            name="teams",
        ),
    re_path(
        r"^v1/teams/%s/$" % PVAR_PROFILE_ID,
        views.TeamViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="teams.action",
        ),
    re_path(
            r"^v1/players/$",
            views.PlayerViewSet.as_view(
                {
                    "get": "list",
                    "post": "create",
                }
            ),
            name="players",
        ),
    re_path(
        r"^v1/players/%s/$" % PVAR_PROFILE_ID,
        views.PlayerViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="players.action",
        ),
]
