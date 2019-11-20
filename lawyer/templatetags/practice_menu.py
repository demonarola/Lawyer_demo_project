from django import template
import datetime
from lawyer.models import Practice_area

register = template.Library()


def practice_area():
    practice = Practice_area.objects.all()
    return practice
register.simple_tag(practice_area)