#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from accounts.models import BaseUser
from django.contrib.auth.models import Permission

print("🔍 Finding existing manager accounts...")

# Check for existing staff users
staff_users = BaseUser.objects.filter(is_staff=True)
print(f"Found {staff_users.count()} staff users:")

for user in staff_users:
    print(f"  - Username: {user.username}")
    print(f"    Email: {user.email}")
    print(f"    Is Staff: {user.is_staff}")
    print(f"    Is Admin: {user.is_admin}")
    print()

# Check if we have a test manager
try:
    test_manager = BaseUser.objects.get(username='manager_test')
    print(f"✅ Test manager found: {test_manager.username}")
    print(f"   Email: {test_manager.email}")
    print(f"   Is Staff: {test_manager.is_staff}")
    print(f"   Is Active: {test_manager.is_active}")
except BaseUser.DoesNotExist:
    print("❌ No test manager found. Creating one...")
    
    # Create test manager
    test_manager = BaseUser.objects.create_user(
        username='manager_test',
        email='manager@test.com',
        password='manager123',
        is_staff=True,
        is_active=True
    )
    
    # Grant basic permissions
    view_permission = Permission.objects.get(codename='view_baseorder')
    test_manager.user_permissions.add(view_permission)
    
    print(f"✅ Test manager created: {test_manager.username}")
    print(f"   Email: {test_manager.email}")
    print(f"   Password: manager123")

print("\n🎯 Manager Login Information:")
print("Username: manager_test")
print("Password: manager123")
print("Login URL: http://localhost:8000/accounts/login/")









