from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='format_time_difference')
def format_time_difference(updated_at):
  now = timezone.now()
  time_difference = now - updated_at

  days = time_difference.days
  months = days // 30
  years = days // 365

  if years >= 1:
    return f'{years} {"year" if years == 1 else "years"}'
  elif months >= 1:
    return f'{months} {"month" if months == 1 else "months"}'
  elif days >= 1:
    return f'{days} {"day" if days == 1 else "days"}'
  else:
    return 'today'
