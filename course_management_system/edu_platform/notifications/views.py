from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import notification_serializer
from .permissions import is_notification_owner
from rest_framework.permissions import IsAuthenticated

class notification_view_set(viewsets.ModelViewSet):
    serializer_class = notification_serializer
    permission_classes = [IsAuthenticated, is_notification_owner]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})