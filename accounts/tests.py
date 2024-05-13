from django.test import TestCase
from google.cloud import storage
from accounts.models import Captcha
# Create your tests here.
from django.core.management.base import BaseCommand
from captcha.image import ImageCaptcha
import random
import string
import os

class SetUpTest(TestCase):
    # Clear existing CAPTCHA images
    Captcha.objects.all().delete()

    # Define CAPTCHA image directory
    # captcha_dir = os.path.join('static', 'captcha')
    # if not os.path.exists(captcha_dir):
    #     os.makedirs(captcha_dir)

    # # Generate and save CAPTCHA images
    # for i in range(1000):
    #     # Generate a random 5-character alphanumeric string for the value
    #     value = ''.join(random.choices(string.digits, k=5))

    #     # Create an ImageCaptcha instance with custom settings
    #     image = ImageCaptcha(width=150, height=50, font_sizes=[30])
    #     image_path = os.path.join(captcha_dir, '{}.png'.format(value))
    #     image.write(value, image_path)
    #     Captcha.objects.create(value=value, image=image_path)

    print("CAPTCHA images generated and saved successfully.")
