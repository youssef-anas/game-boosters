#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from accounts.models import BaseUser, BaseOrder, Captcha
from games.models import Game
from django.contrib.contenttypes.models import ContentType
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder
import random

def create_proper_test_order():
    print("🎮 Creating proper test order with game-specific order...")
    
    # Get test client
    try:
        client = BaseUser.objects.get(username='client_test')
    except BaseUser.DoesNotExist:
        print("❌ Test client not found! Run create_test_users.py first.")
        return
    
    # Get League of Legends game
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
    
    # Create the base order first
    base_order = BaseOrder.objects.create(
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
    
    # Create the game-specific order (League of Legends)
    try:
        # Get some ranks for League of Legends
        from leagueOfLegends.models import LeagueOfLegendsRank
        
        # Get Bronze and Silver ranks
        bronze_rank = LeagueOfLegendsRank.objects.filter(rank_name__icontains='bronze').first()
        silver_rank = LeagueOfLegendsRank.objects.filter(rank_name__icontains='silver').first()
        
        if not bronze_rank or not silver_rank:
            print("⚠️  No ranks found, creating with default values")
            bronze_rank = None
            silver_rank = None
        
        # Create the League of Legends specific order
        lol_order = LeagueOfLegendsDivisionOrder.objects.create(
            order=base_order,
            current_rank=bronze_rank,
            desired_rank=silver_rank,
            current_division=4,  # Bronze IV
            desired_division=1,  # Silver I
            current_marks=0,  # 0-20 LP
            select_champion=False
        )
        
        # Set the content type and object id for the base order
        content_type = ContentType.objects.get_for_model(LeagueOfLegendsDivisionOrder)
        base_order.content_type = content_type
        base_order.object_id = lol_order.pk
        base_order.save()
        
        print("✅ Proper test order created successfully!")
        print(f"   Order ID: {base_order.id}")
        print(f"   Order Name: {base_order.name}")
        print(f"   Game: {game.name}")
        print(f"   Customer: {client.username}")
        print(f"   Price: ${base_order.price}")
        print(f"   Booster Earnings: ${base_order.money_owed}")
        print(f"   Captcha: {captcha.value}")
        print(f"   Status: {base_order.status}")
        print(f"   LOL Order ID: {lol_order.id}")
        print(f"   Content Type: {content_type}")
        
        print("\n🎯 Order is now properly structured and should appear in client orders!")
        print("📋 Next steps:")
        print("1. Refresh the client orders page")
        print("2. Login as booster_test to claim the order")
        print("3. Test the chat system")
        print("4. Complete the order")
        
        return base_order
        
    except Exception as e:
        print(f"❌ Error creating game-specific order: {e}")
        # Clean up the base order if game order creation failed
        base_order.delete()
        return None

if __name__ == '__main__':
    create_proper_test_order()
