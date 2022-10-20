# -*- encoding:utf8 -*-
from flask import request
import MtgCardsService  as cardsService

def top(render_params, data):
    editions = cardsService.getAllEditions()
    
    render_params['editions'] = editions
    render_params["body"] = data["body"]
    render_params["title"] = data["title"]
    return render_params
