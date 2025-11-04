#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from accounts.models import BaseUser
from booster.models import Booster

def reset_booster_password():
    print("🔧 Resetting password for existing booster...")
    
    try:
        # Find a booster that has a profile
        boosters = Booster.objects.all()[:3]
        
        if not boosters:
            print("❌ No boosters with profiles found!")
            return False
        
        # Use the first booster
        booster = boosters[0]
        user = booster.booster
        
        print(f"Found booster: {user.username}")
        print(f"Email: {user.email}")
        
        # Reset password to something simple
        user.set_password('booster123')
        user.save()
        
        print(f"✅ Password reset successfully!")
        print(f"📋 Login Credentials:")
        print(f"   Username: {user.username}")
        print(f"   Password: booster123")
        print(f"   Login URL: http://localhost:8000/accounts/login/")
        
        # Check booster profile
        print(f"\n📋 Booster Profile:")
        print(f"   Can choose me: {booster.can_choose_me}")
        print(f"   LOL player: {booster.is_lol_player}")
        print(f"   Valorant player: {booster.is_valo_player}")
        print(f"   CS:GO player: {booster.is_csgo2_player}")
        
        print(f"\n🎯 Ready to test!")
        print(f"1. Login with: {user.username} / booster123")
        print(f"2. Go to: http://localhost:8000/booster/orders_jobs/")
        print(f"3. Claim the test order")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    reset_booster_password()









