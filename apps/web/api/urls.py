from django.urls import path

from .views import ProcessWebHookAPIView

urlpatterns = [
    path(
        'webhook/<hook_id>/',
        ProcessWebHookAPIView.as_view(),
        name='hooks-handler'
    ),
]
