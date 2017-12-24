from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path(r'api/v1/', include(
        ('apps.web.api.urls', 'apps.web'), namespace='web-api')),
    path(r'admin/', admin.site.urls),

]
