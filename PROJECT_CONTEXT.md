# 🎯 Project Context

This is a Django 5.0.10 project for a game boosting website named **GameBoosterss**.

It supports boosting orders for games like **League of Legends** using an LP/rank system.

---

## ⚙️ Current Features Summary

### 🔹 Real-Time Order Synchronization
- WebSocket support via `Django Channels`
- `realtime` app handles all order-related live updates
- Signal-based updates for:
  - `BaseOrder`
  - `LeagueOfLegendsDivisionOrder`
  - `BoosterTransaction`
- Test endpoint: `/realtime/test/`
- Live updates for:
  - Order status
  - Progress %
  - Price
  - Booster assignment
- Uses `Redis` (with fallback to `InMemoryChannelLayer`)

### 🔹 Chat System Fixes
- Auto-create chat rooms when missing
- Handles booster/admin/customer chats
- Truncation for long names and slugs
- Email sending wrapped with error handling
- Fixed "Room.DoesNotExist" and SMTP issues
- WebSocket group name sanitization for invalid characters

---

## 🧱 Tech Stack

- **Django**: 5.0.10
- **Channels**: 4.1.0
- **ASGI Server**: Daphne
- **Database**: PostgreSQL 13
- **Channel Layer**: Redis (optional, falls back to InMemoryChannelLayer)
- **Frontend**: Django Templates + Tailwind CSS (CDN)

---

## 🚀 Environment Setup

- **ASGI entrypoint**: `gameBoosterss/asgi.py`
- **Main apps**: 
  - `accounts` - User management, orders, transactions
  - `dashboard` - Admin dashboard
  - `customer` - Customer views
  - `chat` - Chat system
  - `realtime` - Real-time synchronization
  - `leagueOfLegends` - LoL-specific order models
- **Redis config**: `docker-compose.yml`
- **Test URLs**:
  - `http://localhost:8000/realtime/test/` - Real-time test page
  - `http://localhost:8000/admin/dashboard/` - Admin dashboard
  - `http://localhost:8000/dashboard/chat/<order_name>/` - Chat page

---

## 📁 Project Structure

```
game-boosters-main/
├── accounts/              # User, Order, Transaction models
├── dashboard/            # Admin dashboard views
├── customer/              # Customer views
├── chat/                  # Chat system (Room, Message models)
│   ├── consumers.py      # ChatConsumer (WebSocket)
│   ├── models.py         # Room, Message models
│   └── routing.py        # WebSocket routes
├── realtime/              # Real-time sync app
│   ├── consumers.py      # OrderSyncConsumer (WebSocket)
│   ├── signals.py        # Order update signals
│   ├── routing.py        # WebSocket routes
│   └── views.py          # Test page view
├── leagueOfLegends/       # LoL-specific models
├── gameBoosterss/         # Project settings
│   ├── settings.py       # Django settings
│   ├── asgi.py           # ASGI configuration
│   └── urls.py           # URL routing
└── requirements.txt      # Dependencies
```

---

## ✅ Your Tasks (for Cursor)

You are now the assistant developer for this project.

### When writing new code:

- ✅ Follow Django best practices
- ✅ Maintain async-safe operations (no blocking DB queries in consumers)
- ✅ Use `database_sync_to_async` for DB operations in async contexts
- ✅ Use `post_save` signals for real-time events
- ✅ Ensure compatibility with `Django Channels` and existing signal system
- ✅ Keep all code **PEP8 compliant**
- ✅ Add concise docstrings for every function/class
- ✅ Handle errors gracefully (try-except blocks)
- ✅ Sanitize group names for WebSocket (ASCII alphanumerics, hyphens, underscores, periods only)
- ✅ Truncate long strings to fit database constraints

### Code Patterns to Follow:

#### WebSocket Consumers
```python
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Use async-safe operations
        await self.channel_layer.group_add(...)
        await self.accept()
    
    @database_sync_to_async
    def get_data(self):
        # DB operations here
        return Model.objects.get(...)
```

#### Signal Handlers
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            'group_name',
            {'type': 'message_type', 'data': 'value'}
        )
```

#### String Sanitization
```python
import re

def sanitize_group_name(name):
    """Sanitize for Django Channels group names (< 100 chars, ASCII alphanumerics only)"""
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
    if len(sanitized) > 94:  # Account for prefix
        sanitized = sanitized[:94]
    return sanitized
```

---

## 🔧 Examples of Future Tasks

1. **Real-time notifications** for multiple orders at once
2. **Authentication & permissions** to WebSockets
3. **Real-time chat typing indicators**
4. **Frontend integration** for dashboards (React/Vue optional)
5. **Optimize Redis usage** for high concurrency
6. **Order history tracking** with real-time updates
7. **Real-time notifications system** for users
8. **Typing indicators** in chat rooms
9. **Online/offline status** updates
10. **Message read receipts**

---

## ⚡ Commands Reference

### Development Server
```bash
# Standard Django development server
python manage.py runserver

# ASGI server (for WebSocket support)
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application

# With migrations
python manage.py migrate
python manage.py migrate --noinput  # Non-interactive
```

### Redis (Optional)
```bash
# Start Redis via Docker
docker compose up -d redis

# Check Redis status
docker compose ps redis
```

### Testing
```bash
# Run tests
python manage.py test

# Test real-time sync
python test_realtime_order_sync.py
```

---

## 🔍 Key Models

### BaseOrder (`accounts/models.py`)
- Main order model
- Fields: `customer`, `booster`, `status`, `price`, `actual_price`, `name`
- Signals: Connected to `realtime/signals.py`

### LeagueOfLegendsDivisionOrder (`leagueOfLegends/models.py`)
- LoL-specific order details
- Fields: `current_rank`, `desired_rank`, `progress`, etc.
- Signals: Connected to `realtime/signals.py`

### Room (`chat/models.py`)
- Chat room model
- Fields: `name`, `slug`, `customer`, `booster`, `order_name`, `is_for_admins`
- Methods: `create_room_with_booster()`, `create_room_with_admins()`
- String truncation: `name` max 50, `slug` max 100, `order_name` max 50

### Message (`chat/models.py`)
- Chat message model
- Fields: `user`, `content`, `room`, `msg_type`, `created_on`

---

## 🐛 Known Issues & Solutions

### Issue: Room DoesNotExist
**Solution**: Use `Room.create_room_with_admins()` or `Room.create_room_with_booster()` instead of `Room.objects.get()`

### Issue: String length validation
**Solution**: Truncate strings in `Room.create_room_with_*()` methods

### Issue: SMTP email errors
**Solution**: Wrap email sending in try-except blocks

### Issue: WebSocket group name validation
**Solution**: Sanitize group names using `sanitize_group_name()` function

---

## 📝 Notes

- **Email Configuration**: Currently optional - chat rooms work without email
- **Redis**: Optional for development - uses InMemoryChannelLayer as fallback
- **String Truncation**: Long order names are automatically truncated
- **Error Handling**: All critical errors are handled gracefully
- **WebSocket Groups**: Must be < 100 chars, ASCII alphanumerics only

---

## 🎯 Quick Reference

- **Real-time sync**: `realtime/consumers.py` → `OrderSyncConsumer`
- **Chat WebSocket**: `chat/consumers.py` → `ChatConsumer`
- **Order signals**: `realtime/signals.py`
- **Test page**: `/realtime/test/`
- **Admin dashboard**: `/admin/dashboard/`

---

**Last Updated**: After WebSocket group name sanitization fix

