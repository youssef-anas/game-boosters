#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')

try:
	import django
	django.setup()
except Exception as e:
	print(f"Failed to setup Django: {e}")
	sys.exit(1)

from accounts.models import BaseUser
from django.contrib.auth.models import Permission

CREDS = {
	"admin": {"username": "admin", "email": "admin@test.com", "password": "admin123"},
	"manager": {"username": "manager_test", "email": "manager@test.com", "password": "manager123"},
	"booster": {"username": "working_booster", "email": "booster@test.com", "password": "working123"},
	"client": {"username": "client_test", "email": "client@test.com", "password": "client123"},
}

def upsert_user(username: str, email: str, password: str, **flags):
	user, created = BaseUser.objects.get_or_create(username=username, defaults={"email": email})
	changes = []
	if created:
		changes.append("created")
		user.email = email
		user.set_password(password)
	for key, value in flags.items():
		if getattr(user, key) != value:
			setattr(user, key, value)
			changes.append(f"{key}={value}")
	if password and not created:
		user.set_password(password)
		changes.append("password_reset")
	user.is_active = True
	user.save()
	return user, created, changes

# Admin
admin_user, _, admin_changes = upsert_user(
	CREDS["admin"]["username"], CREDS["admin"]["email"], CREDS["admin"]["password"],
	is_staff=True, is_superuser=True, is_admin=True
)

# Manager (staff, not superuser)
manager_user, _, manager_changes = upsert_user(
	CREDS["manager"]["username"], CREDS["manager"]["email"], CREDS["manager"]["password"],
	is_staff=True, is_superuser=False, is_admin=False, is_customer=False, is_booster=False
)
# Grant baseline view perms (best-effort)
try:
	view_models = [
		('accounts', 'baseuser'), ('accounts', 'baseorder'), ('accounts', 'transaction'),
		('booster', 'booster'), ('chat', 'message')
	]
	perms = []
	for app_label, model in view_models:
		perm = Permission.objects.get(codename=f"view_{model}")
		perms.append(perm)
	manager_user.user_permissions.add(*perms)
except Exception:
	pass

# Booster
booster_user, _, booster_changes = upsert_user(
	CREDS["booster"]["username"], CREDS["booster"]["email"], CREDS["booster"]["password"],
	is_booster=True, is_customer=False, is_staff=False, is_superuser=False
)

# Client
client_user, _, client_changes = upsert_user(
	CREDS["client"]["username"], CREDS["client"]["email"], CREDS["client"]["password"],
	is_customer=True, is_booster=False, is_staff=False, is_superuser=False
)

print("\nCreated/updated accounts:")
print(f"- Admin:    {admin_user.username} ({', '.join(admin_changes) or 'no changes'})")
print(f"- Manager:  {manager_user.username} ({', '.join(manager_changes) or 'no changes'})")
print(f"- Booster:  {booster_user.username} ({', '.join(booster_changes) or 'no changes'})")
print(f"- Client:   {client_user.username} ({', '.join(client_changes) or 'no changes'})")

print("\nLogin URLs and credentials:")
print("Login URL: http://localhost:8000/accounts/login/")
print(f"- Admin:    {CREDS['admin']['username']} / {CREDS['admin']['password']}")
print(f"- Manager:  {CREDS['manager']['username']} / {CREDS['manager']['password']}")
print(f"- Booster:  {CREDS['booster']['username']} / {CREDS['booster']['password']}")
print(f"- Client:   {CREDS['client']['username']} / {CREDS['client']['password']}")







