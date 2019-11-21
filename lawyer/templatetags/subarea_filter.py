from django import template
import ast 
import re

register = template.Library()

def subarea_list(subarea):
    res = ast.literal_eval(subarea)
    l = []
    for i in res:
        l.append(i)
    return l
register.filter('subarea_list',subarea_list)