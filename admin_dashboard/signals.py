# Django signals for admin_dashboard app
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# This file is required by the admin_dashboard app configuration
# Add any custom signals here as needed for the admin dashboard functionality

# Example signal (uncomment and modify as needed):
# @receiver(post_save, sender=YourModel)
# def your_signal_handler(sender, instance, created, **kwargs):
#     if created:
#         # Handle newly created instance
#         pass
