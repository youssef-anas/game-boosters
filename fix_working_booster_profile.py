#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from accounts.models import BaseUser
from booster.models import Booster

def fix_booster_profile():
    print("🔧 Fixing booster profile for working_booster...")
    
    try:
        # Get the working_booster user
        user = BaseUser.objects.get(username='working_booster')
        print(f"User found: {user.username}")
        
        # Check if booster profile exists
        try:
            booster = Booster.objects.get(booster=user)
            print(f"Booster profile already exists: {booster}")
        except Booster.DoesNotExist:
            print("No booster profile found - creating one...")
            
            # Try to create booster profile with all required fields
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
                print(f"✅ Booster profile created successfully: {booster}")
            except Exception as e:
                print(f"❌ Error creating booster profile: {e}")
                print("This might be due to missing required fields in the database")
                return False
        
        print("\n🎯 Booster profile is ready!")
        print("📋 Now you can:")
        print("1. Login as working_booster / working123")
        print("2. Access http://localhost:8000/booster/orders_jobs/")
        print("3. View and claim available orders")
        
        return True
        
    except BaseUser.DoesNotExist:
        print("❌ working_booster user not found!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    fix_booster_profile()









