from flask import request
import json
import datetime
from dateutil.relativedelta import relativedelta
import services.MtgDecklistService as Decklist

COUNTRY_ID = None

FROM_DATE = datetime.datetime.today() + relativedelta(years=-1)
FROM_DATE = FROM_DATE.strftime('%Y-%m-%d')

def ajaxConstByIdByDate():
    reqJson = request.json
    if 'dmn' in reqJson:
        deck_meta_name = reqJson['dmn']
    else:
        return json.dumps([{"error" : "error"}])
    
    if 'format_id' in reqJson:
        format_id = reqJson['format_id']
    else:
        return json.dumps([{"error" : "error"}])
    
    deck_list_id = Decklist.getDeckIdByName(name)
    
    Decklist.getDecklistAmountByDecklistId(did)
    
def ajaxConstList():
    reqJson = request.json
    if 'dmn' in reqJson:
        deck_meta_name = reqJson['dmn']
    else:
        return json.dumps([{"error" : "error"}])
        
    if 'format_id' in reqJson:
        format_id = reqJson['format_id']
    else:
        return json.dumps([{"error" : "error"}])
        
    result = Decklist.getDecklistByMetaName(deck_meta_name, format_id)
        
    list_graph_data = []
    
    if result is None:
        list_graph_data.append({"error" : "error"})
        return json.dumps(list_graph_data)
    else:
        for u in result:
            list_graph_data.append({
                "error"        : ""
                ,"meta_name"    : deck_meta_name
                ,"player_name" : str(u.player_name)
            })
            break
    
    import sys
    
    
    for u in result:
        list_graph_data.append({
            "board"             : u.which
            ,"amount"           : u.total
            ,"card_name"        : str(u.card_name)
            ,"card_name_en"     : str(u.card_name_en)
            ,"card_type"        : str(u.card_type)
            ,"card_url"         : str(u.card_url)
            ,"image_name"       : str(u.image_name)
        })
    
    return json.dumps(list_graph_data)