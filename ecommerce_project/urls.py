from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from PIL import Image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eshopas_app.urls')), # The change is here
    # Add other app URLs here if you have more apps in the project
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)