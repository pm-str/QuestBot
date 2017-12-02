from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^api/v1/', include('apps.web.api.urls', namespace='web-api')),
    url(r'^admin/', admin.site.urls),

    # url(r'^api/v1/', include('permabots.urls_api', namespace="api")),
    # url(r'^processing/', include('permabots.urls_processing', namespace="permabots")),
]
