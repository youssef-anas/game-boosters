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
from booster.models import Booster
from games.models import Game

username = 'working_booster'
paypal_email = 'booster-paypal@test.com'

user = BaseUser.objects.filter(username=username, is_booster=True).first()
if not user:
	print("Booster user not found or is_booster=False. Run ensure_test_accounts.py first.")
	sys.exit(1)

booster, created = Booster.objects.get_or_create(booster=user, defaults={
	'paypal_account': paypal_email,
	'can_choose_me': True,
})

changes = []
if not booster.paypal_account:
	booster.paypal_account = paypal_email
	changes.append('paypal_account set')

# Enable common game flags so orders can appear
for attr in ['is_lol_player','is_valo_player','is_csgo2_player']:
	if not getattr(booster, attr):
		setattr(booster, attr, True)
		changes.append(f'{attr}=True')

booster.can_choose_me = True
booster.save()

# Optionally attach all existing games for visibility (non-blocking)
try:
	game_ids = list(Game.objects.all().values_list('id', flat=True))
	if game_ids:
		booster.games.set(game_ids)
except Exception:
	pass

print(f"Booster profile {'created' if created else 'updated'} for {username} ({', '.join(changes) or 'no changes'})")







