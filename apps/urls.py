from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path(r'api/v1/', include(
        ('apps.web.api.urls', 'apps.web'), namespace='web-api')),
    path(r'admin/', admin.site.urls),

]
