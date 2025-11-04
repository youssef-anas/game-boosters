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

def section(title: str) -> None:
	print(f"\n=== {title} ===")

def print_user(u: BaseUser) -> None:
	print(f"- {u.id}: {u.username} | {u.email}")

def main() -> None:
	section('Admins (superusers)')
	for u in BaseUser.objects.filter(is_superuser=True):
		print(f"- {u.id}: {u.username} | {u.email} | staff={u.is_staff}")

	section('Managers (staff, not superuser)')
	for u in BaseUser.objects.filter(is_staff=True, is_superuser=False):
		print_user(u)

	section('Boosters')
	for u in BaseUser.objects.filter(is_booster=True):
		print_user(u)

	section('Clients')
	for u in BaseUser.objects.filter(is_customer=True):
		print_user(u)

	print()

if __name__ == '__main__':
	main()







