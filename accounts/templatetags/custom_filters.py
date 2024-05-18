from django import template
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.timezone import now
# from datetime import datetime

register = template.Library()

@register.filter(name='romanize_division')
def romanize_division(value):
  if value == 1:
    return 'IV'
  elif value == 2:
    return 'III'
  elif value == 3:
    return 'II'
  elif value == 4:
    return 'I'
  else:
    return value
  
@register.filter(name='server_name')
def server_name(value):
  if value == 1:
    return 'Europa'
  elif value == 2:
    return 'America'
  elif value == 3:
    return 'Asia'
  elif value == 4:
    return 'Africa'
  elif value == 5:
    return 'Oceania'
  else:
    return value

  
@register.filter(name='romanize_division_original')
def romanize_division_original(value):
  if value == 1:
    return 'I'
  elif value == 2:
    return 'II'
  elif value == 3:
    return 'III'
  elif value == 4:
    return 'IV'
  else:
    return value
  
@register.filter(name='ten_romanize_division')
def ten_romanize_division(value):
  if value == 1:
    return 'X'
  elif value == 2:
    return 'IX'
  elif value == 3:
    return 'VIII'
  elif value == 4:
    return 'VII'
  elif value == 5:
    return 'VI'
  elif value == 6:
    return 'V'
  elif value == 7:
    return 'IV'
  elif value == 8:
    return 'III'
  elif value == 9:
    return 'II'
  elif value == 10:
    return 'I'
  else:
    return value
  
@register.filter(name='five_romanize_division')
def five_romanize_division(value):
  if value == 1:
    return 'V'
  elif value == 2:
    return 'IV'
  elif value == 3:
    return 'III'
  elif value == 4:
    return 'II'
  elif value == 5:
    return 'I'
  else:
    return value
  
@register.filter(name='wow_ranks')
def wow_ranks(value):
  value = float(value)
  if value < 1600:
    return ['0-1599', 1]
  elif value < 1800:
    return ['1600-1799', 2]
  elif value < 2100:
    return ['1800-2099', 3]
  elif value <= 2500:
    return ['2100-2500', 4]
  else:
    return value
  
@register.filter(name='dota2_ranks')
def dota2_ranks(value):
  value = float(value)
  if value <= 700:
    return ['herald', 1]
  elif value <= 1540:
    return ['guardian', 2]
  elif value <= 2380:
    return ['crusader', 3]
  elif value <= 3220:
    return ['archon', 4]
  elif value <= 4060:
    return ['legend', 5]
  elif value <= 4900:
    return ['ancient', 6]
  elif value <= 5500:
    return ['divine', 7]
  elif value > 5500:
    return ['immortal', 8]
  else:
    return value
  
@register.filter(name='csgo2_ranks')
def csgo2_ranks(value):
  value = int(value)
  if value < 5000:
    return ['silver', 1]
  elif value < 10000:
    return ['grey', 2]
  elif value < 15000:
    return ['blue', 3]
  elif value < 20000:
    return ['purple', 4]
  elif value < 25000:
    return ['pink', 5]
  elif value >= 25000:
    return ['red', 6]
  else:
    return value
  
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

#Custom Filter To Time 
@register.filter(name='custom_timesince')
def custom_timesince(value):
  
  if not value:
    return ''

  delta = now() - value

  if delta.total_seconds() < 60:
    return '{} second{} ago'.format(int(delta.total_seconds()), '' if int(delta.total_seconds()) == 1 else 's')
  elif delta.total_seconds() < 3600:
    minutes = int(delta.total_seconds() // 60)
    return '{} minute{} ago'.format(minutes, '' if minutes == 1 else 's')
  elif delta.total_seconds() < 86400:
    hours = int(delta.total_seconds() // 3600)
    return '{} hour{} ago'.format(hours, '' if hours == 1 else 's')
  elif delta.total_seconds() < 2592000:  # 30 days
    days = int(delta.total_seconds() // 86400)
    return '{} day{} ago'.format(days, '' if days == 1 else 's')
  elif delta.total_seconds() < 31536000:  # 365 days
    months = int(delta.total_seconds() // 2592000)  # 30 days per month approximation
    return '{} month{} ago'.format(months, '' if months == 1 else 's')
  else:
    years = int(delta.total_seconds() // 31536000)  # 365 days per year
    return '{} year{} ago'.format(years, '' if years == 1 else 's')
  

@register.filter
def format_date(created_on):
    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)
    
    if created_on.date() == today:
      return 'Today'
    elif created_on.date() == yesterday:
      return 'Yesterday'
    elif created_on.year != today.year:
      return created_on.strftime('%d %B %Y')  # Format as 'day month year' (e.g., '23 March 2023')
    else:
      return created_on.strftime('%d %B')  # Format as 'day month' (e.g., '23 March')
    

@register.filter
def extract_order_from(text):
  start_marker = "From "
  end_marker = " To"
  start_index = text.find(start_marker)
  end_index = text.find(end_marker, start_index + len(start_marker))
  
  if start_index != -1 and end_index != -1:
    return text[start_index + len(start_marker):end_index]
  else:
    return ""
  
@register.filter
def extract_order_to(text):
  start_marker = "To "
  start_index = text.find(start_marker)

  if start_index != -1:
    return text[start_index + len(start_marker):]
  else:
    return ""
  
@register.filter
def first_two_chars(value):
  value_str = str(value)
  return value_str[:2]