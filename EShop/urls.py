
from django.contrib import admin
from django.urls import include, path
from EShop import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('EShop.store.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
