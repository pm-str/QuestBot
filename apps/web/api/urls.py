from rest_framework.routers import SimpleRouter

from .views import ProcessWebHookAPIView

router = SimpleRouter()

router.register(
    'webhook/(?P<hook_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
    ProcessWebHookAPIView,
    'webhook-processing',
)

urlpatterns = router.urls
