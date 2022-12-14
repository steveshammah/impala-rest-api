from django.urls import path, re_path
from . import views

PVAR_PROFILE_ID = r"(?P<lookup_value>[\w\-\@\.\$]+)"
PVAR_TOKEN = r"(?P<token>[\w]+)"

urlpatterns = [
    path('', views.home, name='website-home'),
    path('users/', views.get_all_users, name='users page'),
    path('users/<str:pk>/', views.get_user, name='user page'),
    path('authors/', views.get_all_authors, name='authors page'),
    path('authors/<str:pk>/', views.get_author, name='author page'),
    path('players/', views.get_all_players, name='players page'),
    path('players/<str:pk>/', views.get_player, name='player page'),
    path('articles/', views.get_all_articles, name='articles page'),
    path('articles/<str:pk>/', views.get_article, name='article page'),
    path('article-create/', views.create_article, name='article create'),
    path('article-delete/<str:pk>', views.delete_article, name='article delete'),
    path('article-update/<str:pk>', views.update_article, name='article update'),
    path('products/', views.get_all_products, name='products page'),
    path('products/<str:pk>/', views.get_product, name='product page'),

    # --------- ** CLASS-BASED URLS ** --------#
    path(
        "v1/auth/login/",
        views.AuthViewSet.as_view({"post": "login"}),
    ),
    path(
        "v1/auth/retrieve/",
        views.AuthViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
    path(
        "v1/auth/logout/",
        views.AuthViewSet.as_view(
            {
                "post": "logout",
            }
        ),
    ),
    re_path(
            r"^v1/authors/$",
            views.AuthorViewSet.as_view(
                {
                    "get": "list",
                    "post": "create",
                }
            ),
            name="authors",
        ),
    re_path(
        r"^v1/authors/%s/$" % PVAR_PROFILE_ID,
        views.AuthorViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="authors.action",


        ),
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
    re_path(
            r"^v1/articles/$",
            views.ArticleViewSet.as_view(
                {
                    "get": "list",
                    "post": "create",
                }
            ),
            name="articles",
        ),
    re_path(
        r"^v1/articles/%s/$" % PVAR_PROFILE_ID,
        views.ArticleViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="articles.action",
        ),
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
