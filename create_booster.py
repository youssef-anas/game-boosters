#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import BaseUser
from booster.models import Booster, Language
from games.models import Game

# Create booster user if it doesn't exist
if not User.objects.filter(username='booster_test').exists():
    # Create Django User
    user = User.objects.create_user(
        username='booster_test',
        email='booster@example.com',
        password='booster123',
        first_name='Test',
        last_name='Booster'
    )
    
    # Create BaseUser
    base_user = BaseUser.objects.create(
        user=user,
        username='booster_test',
        email='booster@example.com',
        is_booster=True,
        is_active=True
    )
    
    # Create Booster profile
    booster = Booster.objects.create(
        booster=base_user,
        discord_id='booster_test#1234',
        paypal_account='booster@example.com',
        about_you='I am a professional gaming booster with years of experience.',
        can_choose_me=True
    )
    
    # Add some games (if they exist)
    try:
        # Try to add some common games
        games = Game.objects.all()[:3]  # Get first 3 games
        booster.games.set(games)
        
        # Add some languages
        languages = Language.objects.all()[:2]  # Get first 2 languages
        booster.languages.set(languages)
    except:
        pass  # If no games/languages exist, continue
    
    print("Booster user created successfully!")
    print("Username: booster_test")
    print("Password: booster123")
    print("Email: booster@example.com")
    print("Discord: booster_test#1234")
else:
    print("Booster user already exists!")
    print("Username: booster_test")
    print("Password: booster123")

