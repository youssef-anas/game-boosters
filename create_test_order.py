#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from accounts.models import BaseUser, BaseOrder, Captcha
from games.models import Game
from django.contrib.contenttypes.models import ContentType
import random

def create_test_order():
    print("🎮 Creating test order without payment...")
    
    # Get test client
    try:
        client = BaseUser.objects.get(username='client_test')
    except BaseUser.DoesNotExist:
        print("❌ Test client not found! Run create_test_users.py first.")
        return
    
    # Get a game (preferably League of Legends)
    try:
        game = Game.objects.filter(name__icontains='league').first()
        if not game:
            game = Game.objects.first()
        if not game:
            print("❌ No games found in database!")
            return
    except:
        print("❌ Error getting game!")
        return
    
    # Get a random captcha
    try:
        captcha = Captcha.objects.order_by('?').first()
        if not captcha:
            captcha = Captcha.objects.create(value=str(random.randint(1000, 9999)))
    except:
        captcha = Captcha.objects.create(value=str(random.randint(1000, 9999)))
    
    # Create test order
    order = BaseOrder.objects.create(
        name=f'TEST_ORDER_{random.randint(1000, 9999)}',
        details='Test order for flow testing - Division boost from Bronze to Silver',
        game=game,
        game_type='D',  # Division
        price=25.00,
        actual_price=25.00,
        real_order_price=25.00,
        money_owed=20.00,  # Booster gets 80% (20/25)
        invoice='TEST_INVOICE_NO_PAYMENT',
        status='New',
        customer=client,
        booster=None,  # No booster assigned yet
        customer_gamename='TestSummoner',
        customer_username='testuser123',
        customer_password='testpass123',
        customer_server='EUW',
        captcha=captcha,
        payer_id='TEST_PAYER_ID',
        is_done=False,
        is_drop=False,
        is_extended=False,
        data_correct=True,
        approved=True
    )
    
    print("✅ Test order created successfully!")
    print(f"   Order ID: {order.id}")
    print(f"   Order Name: {order.name}")
    print(f"   Game: {game.name}")
    print(f"   Customer: {client.username}")
    print(f"   Price: ${order.price}")
    print(f"   Booster Earnings: ${order.money_owed}")
    print(f"   Captcha: {captcha.value}")
    print(f"   Status: {order.status}")
    
    print("\n🎯 Order is ready for testing!")
    print("📋 Next steps:")
    print("1. Login as booster_test")
    print("2. Go to orders/jobs to see available orders")
    print("3. Claim the order using the captcha")
    print("4. Test the chat system")
    print("5. Complete the order")
    
    return order

if __name__ == '__main__':
    create_test_order()



