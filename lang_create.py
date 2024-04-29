import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gameBoosterss.settings")
django.setup()

from booster.models import Language

# List of language names
languages_data = [
    'English',
    'العربية',           # Arabic
    '中文',               # Chinese (Simplified)
    'Español',           # Spanish
    'Français',          # French
    'Deutsch',           # German
    'हिन्दी',            # Hindi
    'Italiano',          # Italian
    '日本語',              # Japanese
    '한국어',              # Korean
    'Português',         # Portuguese
    'Русский',           # Russian
    'اردو',               # Urdu
    'Türkçe',            # Turkish
    'Polski',            # Polish
    'ไทย',                 # Thai
    'Nederlands',        # Dutch
    'Svenska',           # Swedish
    'Dansk',             # Danish
    'Suomi',             # Finnish
    'Norsk',             # Norwegian
    'Ελληνικά',          # Greek
    'Magyar',            # Hungarian
    'Čeština',           # Czech
    'Bahasa Indonesia',  # Indonesian
    'עברית',              # Hebrew
    'فارسی',              # Persian
    'Українська',          # Ukrainian
    'Slovenčina',        # Slovak
    'Română',            # Romanian
    'Български',         # Bulgarian
    'Lietuvių',          # Lithuanian
    'Latviešu',          # Latvian
    'Eesti',             # Estonian
    'ქართული',           # Georgian
    'മലയാളം',            # Malayalam
    'తెలుగు',             # Telugu
    'தமிழ்',              # Tamil
    'ਪੰਜਾਬੀ',               # Punjabi
    'اردو',                   # Urdu (again, for a broader audience)
    'ລາວ',                   # Lao
    'ភាសាខ្មែរ',            # Khmer
    'မြန်မာဘာသာ',           # Burmese
    'བོད་སྐད་',               # Tibetan
    'Azərbaycanca',          # Azerbaijani
    'ಕನ್ನಡ',                     # Kannada
    'සිංහල',                  # Sinhala
    'ગુજરાતી',                # Gujarati
    'ଓଡ଼ିଆ',                    # Odia
    'മലയാളം',                      # Malayalam (again, for a broader audience)
    # Add more languages here
]

# Loop through the data and create Language instances if they don't already exist
for language_name in languages_data:
    # Check if the language already exists
    if not Language.objects.filter(language=language_name).exists():
        Language.objects.create(language=language_name)

print("Languages created successfully!")
