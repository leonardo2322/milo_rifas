
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('', include('gestor_rifa.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Si usas debug_toolbar, por ejemplo:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]