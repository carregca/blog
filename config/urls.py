from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Administración · FG"
admin.site.site_title = "Admin FG"
admin.site.index_title = "Panel del blog"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("", include("portfolio.urls")),
]

# En desarrollo Django sirve los archivos subidos (media). En producción lo
# haría el servidor web.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
