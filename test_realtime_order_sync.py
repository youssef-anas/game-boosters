"""
Test script for real-time order synchronization via WebSockets.

This script tests:
1. WebSocket connection opens correctly
2. Order updates trigger group messages
3. Messages are received by connected clients

Usage:
    python test_realtime_order_sync.py
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from accounts.models import BaseOrder, BaseUser
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsRank
from games.models import Game
from realtime.consumers import OrderSyncConsumer
from realtime.signals import send_order_update_to_group
from channels.layers import get_channel_layer
import asyncio
import json


@database_sync_to_async
def get_or_create_test_order():
    """Create a test order for testing"""
    # Get or create a test game (League of Legends)
    game, _ = Game.objects.get_or_create(name='League of Legends', defaults={'id': 4})
    
    # Get or create a test customer
    customer, _ = BaseUser.objects.get_or_create(
        username='test_customer_realtime',
        defaults={
            'email': 'test_customer_realtime@example.com',
            'is_customer': True,
        }
    )
    
    # Get or create a test booster
    booster, _ = BaseUser.objects.get_or_create(
        username='test_booster_realtime',
        defaults={
            'email': 'test_booster_realtime@example.com',
            'is_booster': True,
        }
    )
    
    # Get or create ranks
    rank1, _ = LeagueOfLegendsRank.objects.get_or_create(rank_name='Gold')
    rank2, _ = LeagueOfLegendsRank.objects.get_or_create(rank_name='Platinum')
    
    # Create a test base order
    base_order, created = BaseOrder.objects.get_or_create(
        invoice=f'test_realtime_{asyncio.get_event_loop().time()}',
        defaults={
            'game': game,
            'game_type': 'D',
            'customer': customer,
            'booster': booster,
            'status': 'New',
            'price': 100.0,
            'actual_price': 100.0,
            'real_order_price': 100.0,
            'details': 'Test order for realtime sync',
        }
    )
    
    # Create League of Legends order
    lol_order, _ = LeagueOfLegendsDivisionOrder.objects.get_or_create(
        order=base_order,
        defaults={
            'current_rank': rank1,
            'desired_rank': rank2,
            'current_division': 1,
            'desired_division': 1,
            'current_marks': 0,
        }
    )
    
    return base_order, lol_order


async def test_websocket_connection():
    """Test that WebSocket connection opens correctly"""
    print("\n" + "="*60)
    print("TEST 1: WebSocket Connection")
    print("="*60)
    
    order, _ = await get_or_create_test_order()
    order_id = order.id
    
    # Create WebSocket communicator
    communicator = WebsocketCommunicator(
        OrderSyncConsumer.as_asgi(),
        f"/ws/orders/{order_id}/"
    )
    
    try:
        # Connect
        connected, subprotocol = await communicator.connect()
        assert connected, "WebSocket connection failed"
        print(f"✓ WebSocket connected successfully for order {order_id}")
        
        # Receive initial message
        response = await communicator.receive_json_from()
        assert response['type'] == 'order.update', "Initial message type incorrect"
        assert response['order_id'] == order_id, "Order ID mismatch"
        print(f"✓ Received initial order data: {response}")
        
        return communicator, order_id
        
    except Exception as e:
        print(f"✗ WebSocket connection test failed: {str(e)}")
        raise
    finally:
        await communicator.disconnect()


async def test_order_update_trigger():
    """Test that order updates trigger group messages"""
    print("\n" + "="*60)
    print("TEST 2: Order Update Trigger")
    print("="*60)
    
    order, lol_order = await get_or_create_test_order()
    order_id = order.id
    
    # Create WebSocket communicator
    communicator = WebsocketCommunicator(
        OrderSyncConsumer.as_asgi(),
        f"/ws/orders/{order_id}/"
    )
    
    try:
        # Connect
        connected, _ = await communicator.connect()
        assert connected, "WebSocket connection failed"
        
        # Clear any initial messages
        try:
            await asyncio.wait_for(communicator.receive_json_from(), timeout=1.0)
        except asyncio.TimeoutError:
            pass
        
        # Update order status
        @database_sync_to_async
        def update_order():
            order.status = 'Continue'
            order.save()
            return order
        
        updated_order = await update_order()
        print(f"✓ Updated order status to: {updated_order.status}")
        
        # Wait a bit for the signal to fire
        await asyncio.sleep(0.5)
        
        # Check if we received an update
        try:
            response = await asyncio.wait_for(communicator.receive_json_from(), timeout=2.0)
            assert response['type'] == 'order.update', "Update message type incorrect"
            assert response['status'] == 'Continue', "Status not updated correctly"
            print(f"✓ Received order update: {response}")
            return True
        except asyncio.TimeoutError:
            print("✗ No update message received within timeout")
            return False
        
    except Exception as e:
        print(f"✗ Order update test failed: {str(e)}")
        raise
    finally:
        await communicator.disconnect()


async def test_progress_update():
    """Test that progress updates are broadcasted"""
    print("\n" + "="*60)
    print("TEST 3: Progress Update")
    print("="*60)
    
    order, lol_order = await get_or_create_test_order()
    order_id = order.id
    
    # Create WebSocket communicator
    communicator = WebsocketCommunicator(
        OrderSyncConsumer.as_asgi(),
        f"/ws/orders/{order_id}/"
    )
    
    try:
        # Connect
        connected, _ = await communicator.connect()
        assert connected, "WebSocket connection failed"
        
        # Clear any initial messages
        try:
            await asyncio.wait_for(communicator.receive_json_from(), timeout=1.0)
        except asyncio.TimeoutError:
            pass
        
        # Update LoL order progress
        @database_sync_to_async
        def update_progress():
            # Get a higher rank for reached_rank
            rank2 = LeagueOfLegendsRank.objects.get(rank_name='Platinum')
            lol_order.reached_rank = rank2
            lol_order.reached_division = 2
            lol_order.reached_marks = 2
            lol_order.save()
            return lol_order
        
        updated_lol_order = await update_progress()
        print(f"✓ Updated LoL order progress")
        
        # Wait for signal to fire
        await asyncio.sleep(0.5)
        
        # Check if we received an update
        try:
            response = await asyncio.wait_for(communicator.receive_json_from(), timeout=2.0)
            assert response['type'] == 'order.update', "Update message type incorrect"
            print(f"✓ Received progress update: {response}")
            return True
        except asyncio.TimeoutError:
            print("✗ No progress update message received within timeout")
            return False
        
    except Exception as e:
        print(f"✗ Progress update test failed: {str(e)}")
        raise
    finally:
        await communicator.disconnect()


async def test_multiple_clients():
    """Test that multiple clients receive updates"""
    print("\n" + "="*60)
    print("TEST 4: Multiple Clients")
    print("="*60)
    
    order, _ = await get_or_create_test_order()
    order_id = order.id
    
    # Create multiple WebSocket communicators
    communicators = []
    for i in range(3):
        comm = WebsocketCommunicator(
            OrderSyncConsumer.as_asgi(),
            f"/ws/orders/{order_id}/"
        )
        connected, _ = await comm.connect()
        assert connected, f"Client {i} connection failed"
        
        # Clear initial message
        try:
            await asyncio.wait_for(comm.receive_json_from(), timeout=1.0)
        except asyncio.TimeoutError:
            pass
        
        communicators.append(comm)
    
    print(f"✓ Connected {len(communicators)} clients")
    
    try:
        # Update order
        @database_sync_to_async
        def update_order():
            order.status = 'Done'
            order.save()
            return order
        
        await update_order()
        print(f"✓ Updated order status to: Done")
        
        # Wait for signals
        await asyncio.sleep(0.5)
        
        # Check all clients received update
        received_count = 0
        for i, comm in enumerate(communicators):
            try:
                response = await asyncio.wait_for(comm.receive_json_from(), timeout=2.0)
                if response.get('status') == 'Done':
                    received_count += 1
                    print(f"✓ Client {i} received update")
            except asyncio.TimeoutError:
                print(f"✗ Client {i} did not receive update")
        
        assert received_count == len(communicators), f"Only {received_count}/{len(communicators)} clients received update"
        print(f"✓ All {received_count} clients received the update")
        
    finally:
        for comm in communicators:
            await comm.disconnect()


async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("REALTIME ORDER SYNC TESTS")
    print("="*60)
    
    try:
        # Test 1: WebSocket Connection
        communicator, order_id = await test_websocket_connection()
        await communicator.disconnect()
        
        # Test 2: Order Update Trigger
        await test_order_update_trigger()
        
        # Test 3: Progress Update
        await test_progress_update()
        
        # Test 4: Multiple Clients
        await test_multiple_clients()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        
    except Exception as e:
        print("\n" + "="*60)
        print(f"TESTS FAILED: {str(e)}")
        print("="*60)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    # Run tests
    asyncio.run(run_all_tests())



