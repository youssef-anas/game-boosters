#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from accounts.models import BaseUser
from booster.models import Booster

def fix_booster_profile():
    print("🔧 Fixing booster profile for booster_test...")
    
    try:
        # Get the booster user
        user = BaseUser.objects.get(username='booster_test')
        print(f"User found: {user.username}, is_booster: {user.is_booster}")
        
        # Check if booster profile exists
        try:
            booster = Booster.objects.get(booster=user)
            print(f"Booster profile already exists: {booster}")
            
            # Update the booster profile with required fields
            booster.paypal_account = 'booster@test.com'
            booster.about_you = 'Test booster profile for testing purposes'
            booster.can_choose_me = True
            booster.is_lol_player = True
            booster.is_valo_player = True
            booster.is_csgo2_player = True
            booster.save()
            print("✅ Booster profile updated successfully")
            
        except Booster.DoesNotExist:
            print("No booster profile found - creating one...")
            
            # Create a new booster profile
            booster = Booster.objects.create(
                booster=user,
                paypal_account='booster@test.com',
                about_you='Test booster profile for testing purposes',
                can_choose_me=True,
                is_lol_player=True,
                is_valo_player=True,
                is_csgo2_player=True
            )
            print(f"✅ Booster profile created: {booster}")
        
        print("\n🎯 Booster profile fixed successfully!")
        print("📋 Now you can:")
        print("1. Login as booster_test")
        print("2. Access /booster/orders_jobs/ without errors")
        print("3. View and claim available orders")
        
        return True
        
    except BaseUser.DoesNotExist:
        print("❌ booster_test user not found!")
        return False
    except Exception as e:
        print(f"❌ Error fixing booster profile: {e}")
        return False

if __name__ == '__main__':
    fix_booster_profile()









