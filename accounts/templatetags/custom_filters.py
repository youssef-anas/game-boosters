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
    return value  # return the original value if it doesn't match any condition
