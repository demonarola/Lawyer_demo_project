from django import template
from lawyer.models import Review_Lawyer
from django.db.models import Count,Avg

register = template.Library()

def rates(lid):
    rating_avg = Review_Lawyer.objects.values('lawyer_id__user_id').filter(lawyer_id__user_id=lid).annotate(rates=Avg('rating'))
    for i in rating_avg:
        del i['lawyer_id__user_id']
        x = i.get('rates')
        return round(x,1)
        

register.filter('rates', rates)