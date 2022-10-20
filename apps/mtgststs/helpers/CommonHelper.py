# -*- encoding:utf8 -*-
from flask import request
import random
import re


COLOR_USED = ['#67b7dc']

def generate_random_color():
    r = lambda: random.randint(0,255)
    color = ('#%02X%02X%02X' % (r(),r(),r()))
    if color in COLOR_USED:
        color = generate_random_color()
    else:
        COLOR_USED.append(color)
    return color

def is_Smartphone():
    ua = request.user_agent.string.lower()
    smartphone = ['iphone', 'ipad', 'android', 'android mobile', 'windows phone']
    
    result = False
    for key in smartphone:
        if re.search(key, ua):
            result = True
            break
    
    return result
    

    