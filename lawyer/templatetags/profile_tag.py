from django import template
import datetime
from lawyer.models import Lawyer

register = template.Library()


def profile_menu(lid):
    print(lid)
    try:
        if lid:
            profile = Lawyer.objects.get(user_id=lid)
            return profile.profile_image
    except Exception as e:
        print(e)
register.filter('profile_menu',profile_menu)