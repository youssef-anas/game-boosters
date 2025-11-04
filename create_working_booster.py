#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from accounts.models import BaseUser
from booster.models import Booster
from games.models import Game

def create_working_booster():
    print("🔧 Creating a working booster account...")
    
    try:
        # Check if working booster already exists
        try:
            user = BaseUser.objects.get(username='working_booster')
            print("✅ Working booster already exists!")
            print(f"   Username: {user.username}")
            print(f"   Password: working123")
            print(f"   Login URL: http://localhost:8000/accounts/login/")
            return True
        except BaseUser.DoesNotExist:
            pass
        
        # Create the booster user
        user = BaseUser.objects.create_user(
            username='working_booster',
            email='working_booster@test.com',
            password='working123',
            first_name='Working',
            last_name='Booster',
            is_booster=True,
            is_active=True
        )
        
        print(f"✅ User created: {user.username}")
        
        # Create booster profile with minimal required fields
        try:
            booster = Booster.objects.create(
                booster=user,
                paypal_account='working_booster@test.com',
                about_you='Working booster for testing purposes',
                can_choose_me=True,
                is_lol_player=True,
                is_valo_player=True,
                is_csgo2_player=True
            )
            print(f"✅ Booster profile created: {booster}")
        except Exception as e:
            print(f"⚠️  Booster profile creation failed: {e}")
            print("   But the user account is created and should work for login")
        
        print("\n🎯 Working booster created successfully!")
        print("📋 Login Credentials:")
        print("   Username: working_booster")
        print("   Password: working123")
        print("   Login URL: http://localhost:8000/accounts/login/")
        print("\n📋 Next Steps:")
        print("1. Login with these credentials")
        print("2. Go to: http://localhost:8000/booster/orders_jobs/")
        print("3. Claim the test order")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating working booster: {e}")
        return False

if __name__ == '__main__':
    create_working_booster()









