# create_languages.py

import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gameBoosterss.settings")
django.setup()

from booster.models import Language

# Create instances of Language with default language names
languages_data = [
    {'language': 'English'},
    {'language': 'العربية'},        # Arabic
    {'language': '中文'},            # Chinese (Simplified)
    {'language': 'Español'},        # Spanish
    {'language': 'Français'},       # French
    {'language': 'Deutsch'},        # German
    {'language': 'हिन्दी'},         # Hindi
    {'language': 'Italiano'},       # Italian
    {'language': '日本語'},           # Japanese
    {'language': '한국어'},           # Korean
    {'language': 'Português'},      # Portuguese
    {'language': 'Русский'},        # Russian
    {'language': 'اردو'},            # Urdu
    {'language': 'Türkçe'},         # Turkish
    {'language': 'Polski'},         # Polish
    {'language': 'ไทย'},              # Thai
    {'language': 'Nederlands'},     # Dutch
    {'language': 'Svenska'},        # Swedish
    {'language': 'Dansk'},          # Danish
    {'language': 'Suomi'},          # Finnish
    {'language': 'Norsk'},          # Norwegian
    {'language': 'Ελληνικά'},        # Greek
    {'language': 'Magyar'},         # Hungarian
    {'language': 'Čeština'},        # Czech
    {'language': 'हिन्दी'},         # Hindi (again, for a broader audience)
    {'language': 'Bahasa Indonesia'},  # Indonesian
    {'language': 'עברית'},            # Hebrew
    {'language': 'فارسی'},            # Persian
    {'language': 'Українська'},        # Ukrainian
    {'language': 'Slovenčina'},      # Slovak
    {'language': 'Română'},           # Romanian
    {'language': 'Български'},        # Bulgarian
    {'language': 'Lietuvių'},        # Lithuanian
    {'language': 'Latviešu'},        # Latvian
    {'language': 'Eesti'},           # Estonian
    {'language': 'ქართული'},         # Georgian
    {'language': 'മലയാളം'},            # Malayalam
    {'language': 'తెలుగు'},             # Telugu
    {'language': 'தமிழ்'},              # Tamil
    {'language': 'ਪੰਜਾਬੀ'},               # Punjabi
    {'language': 'اردو'},                   # Urdu (again, for a broader audience)
    {'language': 'ລາວ'},                   # Lao
    {'language': 'ភាសាខ្មែរ'},            # Khmer
    {'language': 'မြန်မာဘာသာ'},           # Burmese
    {'language': 'བོད་སྐད་'},               # Tibetan
    {'language': 'فارسی'},                   # Persian (again, for a broader audience)
]

# Loop through the data and create Language instances
for language_data in languages_data:
    Language.objects.create(**language_data)

print("Languages created successfully!")
