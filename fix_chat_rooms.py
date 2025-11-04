#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from accounts.models import BaseUser
from chat.models import Room, Message

def fix_chat_rooms():
    print("🔧 Fixing chat rooms for test order...")
    
    try:
        # Get the test client and order details
        client = BaseUser.objects.get(username='client_test')
        order_name = 'TEST_ORDER_6045'
        
        print(f"Client: {client.username}")
        print(f"Order: {order_name}")
        
        # Create admin chat room
        admins_chat_slug = f'roomFor-{client.username}-admins-{order_name}'
        print(f"Creating admin room: {admins_chat_slug}")
        
        # Check if admin room already exists
        try:
            admins_room = Room.objects.get(slug=admins_chat_slug)
            print("Admin room already exists")
        except Room.DoesNotExist:
            # Create admin room
            admins_room = Room.objects.create(
                name=f'{client.username}-admins-{order_name}',
                slug=admins_chat_slug,
                customer=client,
                booster=None,
                order_name=order_name,
                is_for_admins=True
            )
            
            # Add welcome messages
            try:
                admin_user = BaseUser.objects.get(id=1)  # System admin user
                Message.create_booster_message(
                    room=admins_room, 
                    message='Welcome, it is honor for us to see you in our site', 
                    sender=admin_user
                )
                Message.create_booster_message(
                    room=admins_room, 
                    message='If you have any questions, do not hesitate to ask', 
                    sender=admin_user
                )
                print("✅ Admin room created with welcome messages")
            except BaseUser.DoesNotExist:
                print("⚠️  Admin user (id=1) not found, creating room without messages")
        
        # Create customer-booster chat room
        customer_booster_slug = f'roomFor-{client.username}-{order_name}'
        print(f"Creating customer-booster room: {customer_booster_slug}")
        
        try:
            customer_booster_room = Room.objects.get(slug=customer_booster_slug)
            print("Customer-booster room already exists")
        except Room.DoesNotExist:
            # Create customer-booster room
            customer_booster_room = Room.objects.create(
                name=f'{client.username}-{order_name}',
                slug=customer_booster_slug,
                customer=client,
                booster=None,  # No booster assigned yet
                order_name=order_name,
                is_for_admins=False
            )
            
            # Add waiting message
            try:
                admin_user = BaseUser.objects.get(id=1)
                Message.create_booster_message(
                    room=customer_booster_room, 
                    message='One of our booster will join chat soon...', 
                    sender=admin_user
                )
                print("✅ Customer-booster room created with waiting message")
            except BaseUser.DoesNotExist:
                print("⚠️  Admin user (id=1) not found, creating room without messages")
        
        print("\n🎯 Chat rooms fixed successfully!")
        print("📋 Now you can:")
        print("1. Click 'Open Order' - it should work now")
        print("2. Access the chat system")
        print("3. Test the complete flow")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing chat rooms: {e}")
        return False

if __name__ == '__main__':
    fix_chat_rooms()









