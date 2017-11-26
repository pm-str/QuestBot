import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class ProcessWebHookAPIView(APIView):
    def post(self, request, hook_id):
        logger.debug('Telegram bot {} got webhook {}'.format(
            request.data,
            hook_id,
        ))

        return Response(status=status.HTTP_201_CREATED)
