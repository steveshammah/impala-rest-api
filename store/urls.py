from django.urls import path, re_path
from . import views

PVAR_PROFILE_ID = r"(?P<lookup_value>[\w\-\@\.\$]+)"
PVAR_TOKEN = r"(?P<token>[\w]+)"

urlpatterns = [
    re_path(
            r"^v1/products/$",
            views.ProductViewSet.as_view(
                {
                    "get": "list",
                    "post": "create",
                }
            ),
            name="products",
        ),
    re_path(
        r"^v1/products/%s/$" % PVAR_PROFILE_ID,
        views.ProductViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="products.action",
        ),
]
