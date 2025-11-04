# Frontend WebSocket Integration Guide

This guide shows how to integrate real-time order synchronization in your frontend dashboards.

## WebSocket Endpoint

Connect to: `ws://<your-domain>/ws/orders/<order_id>/`

Example: `ws://localhost:8000/ws/orders/123/`

## JavaScript Example

### Basic Connection

```javascript
// Connect to WebSocket for a specific order
function connectOrderWebSocket(orderId) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/orders/${orderId}/`;
    
    const socket = new WebSocket(wsUrl);
    
    socket.onopen = function(event) {
        console.log('WebSocket connected for order', orderId);
    };
    
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        if (data.type === 'order.update') {
            updateOrderUI(data);
        }
    };
    
    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
    };
    
    socket.onclose = function(event) {
        console.log('WebSocket closed, reconnecting...');
        // Reconnect after 3 seconds
        setTimeout(() => connectOrderWebSocket(orderId), 3000);
    };
    
    return socket;
}
```

### Update UI Function

```javascript
function updateOrderUI(data) {
    // Update status
    const statusElement = document.querySelector(`[data-order-id="${data.order_id}"] .order-status`);
    if (statusElement) {
        statusElement.textContent = data.status;
        statusElement.classList.add('updated'); // Add animation class
        
        // Show toast notification
        showToast(`Order #${data.order_id}: Status updated to ${data.status} 🎮`);
        
        // Remove animation class after animation
        setTimeout(() => statusElement.classList.remove('updated'), 1000);
    }
    
    // Update progress bar
    const progressBar = document.querySelector(`[data-order-id="${data.order_id}"] .progress-bar`);
    if (progressBar && data.progress !== undefined) {
        progressBar.style.width = `${data.progress}%`;
        progressBar.setAttribute('aria-valuenow', data.progress);
        
        const progressText = document.querySelector(`[data-order-id="${data.order_id}"] .progress-text`);
        if (progressText) {
            progressText.textContent = `${data.progress}%`;
        }
        
        // Show toast notification
        showToast(`Order #${data.order_id}: Progress updated to ${data.progress}% 🎮`);
    }
    
    // Update price
    const priceElement = document.querySelector(`[data-order-id="${data.order_id}"] .booster-price`);
    if (priceElement && data.booster_price) {
        priceElement.textContent = `$${parseFloat(data.booster_price).toFixed(2)}`;
    }
    
    // Update booster info
    if (data.booster_username) {
        const boosterElement = document.querySelector(`[data-order-id="${data.order_id}"] .booster-name`);
        if (boosterElement) {
            boosterElement.textContent = data.booster_username;
        }
    }
    
    // Update reached rank/division (for League of Legends)
    if (data.reached_rank) {
        const rankElement = document.querySelector(`[data-order-id="${data.order_id}"] .reached-rank`);
        if (rankElement) {
            rankElement.textContent = `${data.reached_rank} ${data.reached_division || ''}`;
        }
    }
}
```

### Toast Notification Function

```javascript
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    // Add to page
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
```

### CSS for Toast Notifications

```css
.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 24px;
    background: #4CAF50;
    color: white;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    opacity: 0;
    transform: translateX(100%);
    transition: all 0.3s ease;
    z-index: 10000;
}

.toast.show {
    opacity: 1;
    transform: translateX(0);
}

.toast-info {
    background: #2196F3;
}

.toast-success {
    background: #4CAF50;
}

.toast-warning {
    background: #FF9800;
}

.toast-error {
    background: #F44336;
}

/* Animation for updated elements */
.updated {
    animation: pulse 0.5s ease;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
```

## React Example

```jsx
import { useEffect, useState } from 'react';

function useOrderWebSocket(orderId) {
    const [orderData, setOrderData] = useState(null);
    const [connected, setConnected] = useState(false);
    
    useEffect(() => {
        if (!orderId) return;
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/orders/${orderId}/`;
        
        const socket = new WebSocket(wsUrl);
        
        socket.onopen = () => {
            setConnected(true);
            console.log('WebSocket connected for order', orderId);
        };
        
        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'order.update') {
                setOrderData(data);
                // Show toast notification
                showToast(`Order #${orderId}: Updated!`);
            }
        };
        
        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            setConnected(false);
        };
        
        socket.onclose = () => {
            setConnected(false);
            // Reconnect after 3 seconds
            setTimeout(() => {
                // Reconnect logic here
            }, 3000);
        };
        
        return () => {
            socket.close();
        };
    }, [orderId]);
    
    return { orderData, connected };
}

// Usage in component
function OrderCard({ orderId }) {
    const { orderData, connected } = useOrderWebSocket(orderId);
    
    return (
        <div className="order-card">
            <div className="connection-status">
                {connected ? '🟢 Connected' : '🔴 Disconnected'}
            </div>
            {orderData && (
                <>
                    <div className="order-status">{orderData.status}</div>
                    <div className="progress-bar" style={{ width: `${orderData.progress}%` }}>
                        {orderData.progress}%
                    </div>
                    <div className="booster-price">${parseFloat(orderData.booster_price).toFixed(2)}</div>
                </>
            )}
        </div>
    );
}
```

## Vue.js Example

```vue
<template>
  <div class="order-card">
    <div class="connection-status">
      {{ connected ? '🟢 Connected' : '🔴 Disconnected' }}
    </div>
    <div v-if="orderData">
      <div class="order-status">{{ orderData.status }}</div>
      <div class="progress-bar" :style="{ width: `${orderData.progress}%` }">
        {{ orderData.progress }}%
      </div>
      <div class="booster-price">${{ parseFloat(orderData.booster_price).toFixed(2) }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderCard',
  props: {
    orderId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      orderData: null,
      connected: false,
      socket: null
    }
  },
  mounted() {
    this.connectWebSocket();
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  },
  methods: {
    connectWebSocket() {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/ws/orders/${this.orderId}/`;
      
      this.socket = new WebSocket(wsUrl);
      
      this.socket.onopen = () => {
        this.connected = true;
        console.log('WebSocket connected for order', this.orderId);
      };
      
      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'order.update') {
          this.orderData = data;
          this.showToast(`Order #${this.orderId}: Updated!`);
        }
      };
      
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.connected = false;
      };
      
      this.socket.onclose = () => {
        this.connected = false;
        setTimeout(() => this.connectWebSocket(), 3000);
      };
    },
    showToast(message) {
      // Implement toast notification
      console.log(message);
    }
  }
}
</script>
```

## Message Format

The WebSocket sends messages in the following format:

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

## Integration Points

### Client Dashboard
- Connect to WebSocket when viewing order details
- Update progress bar and status in real-time
- Show toast notifications for updates

### Booster Dashboard
- Connect to WebSocket for all assigned orders
- Highlight "Order Updated" when client or admin makes changes
- Update order cards automatically

### Manager Dashboard
- Connect to WebSocket for all orders in progress
- Automatically update "Orders In Progress" table
- Show real-time status changes

### Admin Dashboard
- Connect to WebSocket for all orders
- Monitor order updates across all dashboards
- Track real-time changes

## Error Handling

Always implement reconnection logic:

```javascript
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

function connectWithRetry(orderId) {
    const socket = connectOrderWebSocket(orderId);
    
    socket.onclose = () => {
        if (reconnectAttempts < maxReconnectAttempts) {
            reconnectAttempts++;
            setTimeout(() => connectWithRetry(orderId), 3000 * reconnectAttempts);
        } else {
            console.error('Max reconnection attempts reached');
        }
    };
    
    socket.onopen = () => {
        reconnectAttempts = 0; // Reset on successful connection
    };
}
```

## Security Considerations

- WebSocket connections are authenticated via Django's authentication middleware
- Only authenticated users can connect
- Origin validation is enforced via `AllowedHostsOriginValidator`
- Use `wss://` for production (HTTPS)



