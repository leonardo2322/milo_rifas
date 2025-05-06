
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from gestor_rifa.manager_errors import mi_error_404, mi_error_500, mi_error_403, mi_error_400
urlpatterns = [
    path('', include('gestor_rifa.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

    # Si usas debug_toolbar, por ejemplo:
handler404 = mi_error_404
handler500 = mi_error_500
handler403 = mi_error_403
handler400 = mi_error_400