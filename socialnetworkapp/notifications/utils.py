from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from esocialnetworkapi.models import Notification
from django.utils import timezone

channel_layer = get_channel_layer()

def create_and_send_notification(recipient, message, notif_type, actor, link=None):
    # Lưu vào DB
    notif = Notification.objects.create(
        recipient=recipient,
        message=message,
        link=link,
        notification_type=notif_type,
        created_at=timezone.now(),
        actor=actor,
    )

    # Gửi qua WebSocket tới user
    async_to_sync(channel_layer.group_send)(
        f"user_{recipient.id}",
        {
            "type": "send_notification",
            "notification": {
                "id": notif.id,
                "message": notif.message,
                "link": notif.link,
                "notification_type": notif.notification_type,
                "is_read": notif.is_read,
                "created_at": notif.created_at.isoformat(),
                "actor_avatar": notif.actor.avatar.url if (notif.actor and notif.actor.avatar) else None,
                "actor_first_name":notif.actor.first_name,
                "actor_last_name": notif.actor.last_name,
            },
        },
    )


