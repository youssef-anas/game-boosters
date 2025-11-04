#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import BaseUser, Wallet
from booster.models import Booster, Language
from games.models import Game
from accounts.models import Captcha
import random

def create_test_users():
    print("🚀 Creating test users for order flow testing...")
    
    # Create test client
    if not BaseUser.objects.filter(username='client_test').exists():
        client = BaseUser.objects.create_user(
            username='client_test',
            email='client@test.com',
            password='client123',
            first_name='Test',
            last_name='Client',
            is_customer=True,
            is_active=True
        )
        
        # Create wallet for client
        Wallet.objects.get_or_create(user=client)
        print("✅ Test client created!")
        print("   Username: client_test")
        print("   Password: client123")
        print("   Email: client@test.com")
    else:
        print("ℹ️  Test client already exists!")
    
    # Create test booster
    if not BaseUser.objects.filter(username='booster_test').exists():
        booster_user = BaseUser.objects.create_user(
            username='booster_test',
            email='booster@test.com',
            password='booster123',
            first_name='Test',
            last_name='Booster',
            is_booster=True,
            is_active=True
        )
        
        # Create wallet for booster
        Wallet.objects.get_or_create(user=booster_user)
        
        # Create booster profile with required fields
        booster = Booster.objects.create(
            booster=booster_user,
            discord_id='booster_test#1234',
            paypal_account='booster@test.com',
            about_you='I am a professional gaming booster for testing purposes.',
            can_choose_me=True,
            is_lol_player=True,  # Enable League of Legends
            is_valo_player=True,  # Enable Valorant
            is_csgo2_player=True  # Enable CS:GO 2
        )
        
        # Add some games to booster (if they exist)
        try:
            games = Game.objects.all()[:3]  # Get first 3 games
            booster.games.set(games)
            print(f"   Added {len(games)} games to booster")
        except:
            print("   No games available to add to booster")
        
        print("✅ Test booster created!")
        print("   Username: booster_test")
        print("   Password: booster123")
        print("   Email: booster@test.com")
        print("   Discord: booster_test#1234")
    else:
        print("ℹ️  Test booster already exists!")
        # Make sure the booster has the required game flags
        try:
            booster_user = BaseUser.objects.get(username='booster_test')
            booster = Booster.objects.get(booster=booster_user)
            booster.is_lol_player = True
            booster.is_valo_player = True
            booster.is_csgo2_player = True
            booster.save()
            print("   Updated booster with required game flags")
        except:
            print("   Could not update booster profile")
    
    # Create some captchas for testing
    captcha_count = Captcha.objects.count()
    if captcha_count < 10:
        for i in range(10 - captcha_count):
            Captcha.objects.create(value=str(random.randint(1000, 9999)))
        print("✅ Created test captchas!")
    
    print("\n🎯 Test users ready! You can now test the complete order flow.")
    print("\n📋 Next steps:")
    print("1. Login as client_test to create an order")
    print("2. Login as booster_test to claim the order")
    print("3. Test the chat system between them")
    print("4. Monitor everything from admin dashboard")

if __name__ == '__main__':
    create_test_users()
