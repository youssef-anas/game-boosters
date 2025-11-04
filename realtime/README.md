# Real-Time Order Synchronization

This Django app provides real-time WebSocket synchronization for order updates across Client, Booster, Manager, and Admin dashboards.

## Features

- **Real-time Updates**: Order status, progress, and price updates are instantly broadcasted to all connected clients
- **WebSocket Support**: Uses Django Channels with Redis for scalable WebSocket connections
- **Automatic Signal Handling**: Django signals automatically emit updates when orders change
- **League of Legends Support**: Special handling for LoL division orders with progress tracking
- **Comprehensive Logging**: All WebSocket events are logged to `/app/logs/realtime.log`

## Architecture

### Components

1. **Consumer** (`consumers.py`): Handles WebSocket connections and message broadcasting
2. **Signals** (`signals.py`): Emits WebSocket updates when models are saved
3. **Routing** (`routing.py`): Defines WebSocket URL patterns
4. **App Config** (`apps.py`): Registers signals when app is ready

### Models Monitored

- `BaseOrder`: Base order model - all order updates trigger WebSocket messages
- `LeagueOfLegendsDivisionOrder`: LoL-specific order updates with progress tracking
- `Transaction`: Transaction updates are broadcasted if related to an order

## WebSocket Endpoint

```
ws://<your-domain>/ws/orders/<order_id>/
```

### Message Format

```json
{
  "type": "order.update",
  "order_id": 123,
  "status": "Continue",
  "progress": 75,
  "booster_price": "85.50",
  "actual_price": "100.00",
  "booster_id": 456,
  "booster_username": "pro_booster",
  "reached_rank": "Platinum",
  "reached_division": 2,
  "reached_marks": 1,
  "message": "Order updated",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Installation

### 1. Dependencies

The following packages are required (already added to `requirements.txt`):

- `channels==4.1.0`
- `channels-redis==4.1.0`
- `daphne==4.1.2`

### 2. Configuration

The app is already registered in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'realtime.apps.RealtimeConfig',
]
```

### 3. Redis Setup

Redis is required for channel layers. Update `docker-compose.yml` includes Redis service:

```yaml
redis:
  image: redis:latest
  restart: always
  ports:
    - "6379:6379"
```

### 4. Channel Layer Configuration

In `settings.py`:

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    }
}
```

### 5. ASGI Routing

The WebSocket routes are automatically included in `asgi.py`:

```python
from realtime.routing import websocket_urlpatterns as realtime_websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                # ... other routes
                *realtime_websocket_urlpatterns,
            ])
        ),
    ),
})
```

### 6. Server Command

Update your deployment command to use Daphne:

```bash
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

## Testing

Run the test script:

```bash
python test_realtime_order_sync.py
```

This tests:
1. WebSocket connection opens correctly
2. Order updates trigger group messages
3. Progress updates are broadcasted
4. Multiple clients receive updates

## Frontend Integration

See `FRONTEND_INTEGRATION.md` for detailed examples in:
- Vanilla JavaScript
- React
- Vue.js

## Logging

Real-time events are logged to:
- Console: All events
- File: `/app/logs/realtime.log` (rotating, 5MB max, 5 backups)

Log levels:
- `DEBUG`: Detailed connection and message logs
- `INFO`: Connection/disconnection events
- `ERROR`: Error messages with full traceback

## Deployment

### Docker Compose

The `docker-compose.yml` includes:
- Redis service
- Web service using Daphne
- Health checks for both services

### Environment Variables

Set these in your `.env` file:

```env
REDIS_HOST=redis
REDIS_PORT=6379
```

For local development:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Troubleshooting

### WebSocket Connection Fails

1. Check Redis is running: `redis-cli ping`
2. Verify channel layer configuration in `settings.py`
3. Check logs: `tail -f logs/realtime.log`
4. Ensure Daphne is running (not `runserver`)

### Messages Not Received

1. Verify signal handlers are registered (check `apps.py`)
2. Check channel layer is not None in logs
3. Verify order ID is correct in WebSocket URL
4. Check browser console for WebSocket errors

### Redis Connection Issues

1. Verify Redis is accessible: `redis-cli -h <host> -p <port> ping`
2. Check firewall rules
3. Verify `REDIS_HOST` and `REDIS_PORT` environment variables

## Performance Considerations

- **Channel Layer**: Uses Redis for scalability across multiple server instances
- **Async Consumers**: All consumers are async for better performance
- **Signal Optimization**: Signals only fire on actual saves (not creates in some cases)
- **Connection Limits**: No built-in limits, but consider rate limiting for production

## Security

- **Authentication**: WebSocket connections are authenticated via Django's auth middleware
- **Origin Validation**: `AllowedHostsOriginValidator` enforces origin validation
- **HTTPS/WSS**: Use `wss://` in production (HTTPS required)

## Future Enhancements

- [ ] Add connection rate limiting
- [ ] Implement WebSocket authentication token
- [ ] Add order update history/audit log
- [ ] Support for multiple game types beyond LoL
- [ ] Add WebSocket connection monitoring dashboard



