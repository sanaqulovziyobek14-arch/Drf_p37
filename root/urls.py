from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.messages import api
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
                  path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
                  path('admin/', admin.site.urls),
                  path('api/v1/', include('apps.urls')),
                  path("ckeditor5/", include('django_ckeditor_5.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


