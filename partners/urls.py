from django.urls import path, re_path
from . import views

PVAR_PROFILE_ID = r"(?P<lookup_value>[\w\-\@\.\$]+)"
PVAR_TOKEN = r"(?P<token>[\w]+)"

urlpatterns = [
    re_path(
            r"^v1/partners/$",
            views.PartnerViewSet.as_view(
                {
                    "get": "list",
                    "post": "create",
                }
            ),
            name="partners",
        ),
    re_path(
        r"^v1/partners/%s/$" % PVAR_PROFILE_ID,
        views.PartnerViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="partners.action",
        ),
]
