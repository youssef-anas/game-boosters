import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from test_lol_pricing import main

if __name__ == '__main__':
    main()


