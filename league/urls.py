from django.urls import path, re_path
from . import views

PVAR_PROFILE_ID = r"(?P<lookup_value>[\w\-\@\.\$]+)"
PVAR_TOKEN = r"(?P<token>[\w]+)"

urlpatterns = [
    re_path(
            r"^v1/fixtures/$",
            views.FixtureViewSet.as_view(
                {
                    "get": "list",
                    "post": "create",
                }
            ),
            name="fixtures",
        ),
    re_path(
        r"^v1/fixtures/%s/$" % PVAR_PROFILE_ID,
        views.FixtureViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="fixtures.action",
        ),
    re_path(
            r"^v1/fixture_results/$",
            views.FixtureResultViewSet.as_view(
                {
                    "get": "list",
                    "post": "create",
                }
            ),
            name="fixture_results",
        ),
    re_path(
        r"^v1/fixture_results/%s/$" % PVAR_PROFILE_ID,
        views.FixtureResultViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="fixture_results.action",
        ),
]
