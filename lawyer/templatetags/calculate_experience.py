from django import template
import datetime

register = template.Library()

def experience(bday, d=None):
    if d is None:
        d = datetime.date.today().year
    return int(d) - int(bday)

register.filter('experience', experience)