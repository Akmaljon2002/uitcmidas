import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

from user.views import login_user_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    path('api/login/', login_user_token, name='login'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('admins/', include('admins.urls')),
    path('user/', include('user.urls')),
    path('sellers/', include('sellers.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
