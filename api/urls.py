from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('home.urls')),
    path('api/auth/', include('members.urls')),
    path('api/league/', include('league.urls')),
    path('api/teamplayer/', include('teamplayer.urls')),
    path('api/officiating/', include('officiating.urls')),
    path('api/store/', include('store.urls')),
    path('api/paymentsubs/', include('paymentsubs.urls')),
    path('api/partners/', include('partners.urls')),
    path('api/messaging/', include('messaging.urls')),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)