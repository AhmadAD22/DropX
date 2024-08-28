from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.app_config import AppConfigSerializer,AppConfig


class AppConfigAPIView(APIView):
    def get(self, request):
        try:
            app_config = AppConfig.objects.first()  # Assuming there is only one instance
            if app_config:
                serializer = AppConfigSerializer(app_config)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Not found'}, status=404)
        except Exception as e:
            return Response({'detail': str(e)}, status=500)