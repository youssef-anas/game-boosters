import json
import pytest
from channels.testing import WebsocketCommunicator
from gameBoosterss.asgi import application
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@pytest.mark.asyncio
async def test_notifications_connects():
    communicator = WebsocketCommunicator(application, "/ws/notifications/admin/")
    connected, _ = await communicator.connect()
    assert connected
    # Initial hello
    msg = await communicator.receive_from()
    data = json.loads(msg)
    assert data["type"] == "notification"
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_notifications_broadcast():
    communicator = WebsocketCommunicator(application, "/ws/notifications/booster/")
    connected, _ = await communicator.connect()
    assert connected

    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        "notifications_booster",
        {
            "type": "notification",
            "title": "Test",
            "message": "Hello booster",
            "timestamp": "2025-11-03T14:12:00Z",
        },
    )

    msg = await communicator.receive_from()
    data = json.loads(msg)
    # First message might be hello, receive until we get our test title
    if data.get("title") != "Test":
        msg = await communicator.receive_from()
        data = json.loads(msg)
    assert data["title"] == "Test"
    assert data["message"] == "Hello booster"
    await communicator.disconnect()



