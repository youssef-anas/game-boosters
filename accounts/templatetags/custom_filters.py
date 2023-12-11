from django import template

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
    return 'Australia'
  else:
    return value