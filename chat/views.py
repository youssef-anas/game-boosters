from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import BaseUser
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from accounts.templatetags.custom_filters import custom_timesince

class StatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = BaseUser.objects.get(id=user_id)
            if user.is_online:
                return Response({'status': 'Online'}, status=status.HTTP_200_OK)
            else:
                # current_time = timezone.now()
                # user_last_online = user.last_online.astimezone(timezone.get_current_timezone())
                user_last_online = user.last_online
                last_seen = custom_timesince(user_last_online)
                # time_diff = current_time-user_last_online
                # time_diff_min = round(time_diff.total_seconds() / 60)
                return Response({'status': last_seen}, status=status.HTTP_200_OK)
        except BaseUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
