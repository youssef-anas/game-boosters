from django.urls import path
from chat.views import StatusAPIView


urlpatterns = [
    path('status/<int:user_id>/', StatusAPIView.as_view(), name='chat.status'),
]