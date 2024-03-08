from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import BaseUser
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class StatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = BaseUser.objects.get(id=user_id)
            if user.is_online:
                return Response({'status': 'online'}, status=status.HTTP_200_OK)
            else:
                current_time = timezone.now()
                user_last_online = user.last_online.astimezone(timezone.get_current_timezone())
                time_diff = current_time-user_last_online
                time_diff_min = round(time_diff.total_seconds()/60)
                return Response({'status': time_diff_min}, status=status.HTTP_200_OK)
        except BaseUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
