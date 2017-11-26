from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import ProcessWebHookAPIView


urlpatterns = [
    url('webhook/(?P<hook_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/',
        csrf_exempt(ProcessWebHookAPIView),
        name='webhook-processing'),
]
