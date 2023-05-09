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
]
