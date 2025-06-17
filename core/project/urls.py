import logging
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


logger = logging.getLogger(__name__)
logger.debug('디버깅 메세지')
logger.info('인포 메세지')
logger.warning('워닝 메세지')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.api.urls')),
    path('manager/', include('core.products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
