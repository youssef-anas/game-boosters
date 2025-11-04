#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from accounts.models import BaseUser
from django.contrib.auth import authenticate

def find_working_booster():
    print("🔍 Finding working booster credentials...")
    
    try:
        # Get all booster users
        boosters = BaseUser.objects.filter(is_booster=True)[:5]
        print(f"Found {boosters.count()} boosters")
        
        # Common passwords to try
        common_passwords = [
            '123456',
            'password', 
            'admin',
            'test',
            'test123',
            'booster',
            'booster123'
        ]
        
        working_boosters = []
        
        for booster in boosters:
            print(f"\nTesting booster: {booster.username}")
            print(f"Email: {booster.email}")
            print(f"Active: {booster.is_active}")
            
            for password in common_passwords:
                try:
                    auth = authenticate(username=booster.username, password=password)
                    if auth:
                        print(f"✅ SUCCESS! Username: {booster.username}, Password: {password}")
                        working_boosters.append((booster.username, password))
                        break
                    else:
                        print(f"❌ Password '{password}': FAILED")
                except Exception as e:
                    print(f"❌ Error testing password '{password}': {e}")
        
        if working_boosters:
            print(f"\n🎯 Found {len(working_boosters)} working booster(s):")
            for username, password in working_boosters:
                print(f"   Username: {username}")
                print(f"   Password: {password}")
                print(f"   Login URL: http://localhost:8000/accounts/login/")
        else:
            print("\n❌ No working booster credentials found with common passwords")
            print("💡 Try using the admin panel to reset a booster's password")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    find_working_booster()









