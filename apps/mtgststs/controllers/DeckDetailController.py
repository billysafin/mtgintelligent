# -*- encoding:utf8 -*-
from flask import request
import services.MtgDecklistService as Decklist
from Main import utils
import re
from Main import config
from helpers.CommonHelper import is_Smartphone
from helpers.LineChartCreator import create as lineChartCreate
from datetime import date
from dateutil.relativedelta import relativedelta

def processDecklists(decklists):
    decklists_modified = []
    mainLands          = []
    mainLandsTotal     = 0
    mainCreatures      = []
    mainCreaturesTotal = 0
    mainSpells         = []
    mainSpellsTotal    = 0
    sideBoard          = []
    checked            = []
    i                  = 1
    sideboardTotal     = 0
    total_dict_count   = len(decklists)
    
    for u in decklists:
        if len(checked) > 0:
            if str(u.player_name) != checked['player_name'] or i == total_dict_count:
                decklists_modified.append({
                    "player_name"  : checked['player_name']
                    ,"date"        : date['date']
                    ,"decklist"    : {
                        "mainLands"            : mainLands
                        ,"mainCreatures"       : mainCreatures
                        , "mainSpells"         : mainSpells
                        , "sideBoard"          : sideBoard
                        ,"mainLandsTotal"      : mainLandsTotal
                        ,"mainCreaturesTotal"  : mainCreaturesTotal
                        ,"mainSpellsTotal"     : mainSpellsTotal
                        ,"sideboardTotal"      : sideboardTotal
                    }
                })

                mainLands          = []
                mainLandsTotal     = 0
                mainCreatures      = []
                mainCreaturesTotal = 0
                mainSpells         = []
                mainSpellsTotal    = 0
                sideBoard          = []
                checked            = {}
                sideboardTotal     = 0
            
        checked = {"player_name"  : str(u.player_name)}
        date = {"date"            : str(u.date)}

        if u.which is 1:
            if re.search(r'Land', str(u.card_type)):
                mainLands.append({
                    "amount"          : u.total
                    ,"card_name"      : str(u.card_name)
                    ,"card_name_en"   : str(u.card_name_en)
                    ,"card_url"       : str(u.card_url)
                    ,"image_name"     : str(u.image_name)
                })
                mainLandsTotal += u.total
            elif re.search(r'Creature', str(u.card_type)):
                mainCreatures.append({
                    "amount"          : u.total
                    ,"card_name"      : str(u.card_name)
                    ,"card_name_en"   : str(u.card_name_en)
                    ,"card_url"       : str(u.card_url)
                    ,"image_name"     : str(u.image_name)
                })
                mainCreaturesTotal += u.total
            else:
                mainSpells.append({
                    "amount"          : u.total
                    ,"card_name"      : str(u.card_name)
                    ,"card_name_en"   : str(u.card_name_en)
                    ,"card_url"       : str(u.card_url)
                    ,"image_name"     : str(u.image_name)
                })
                mainSpellsTotal += u.total
        else:
            sideBoard.append({
                "amount"          : u.total
                ,"card_name"      : str(u.card_name)
                ,"card_name_en"   : str(u.card_name_en)
                ,"card_url"       : str(u.card_url)
                ,"image_name"     : str(u.image_name)
            })
            sideboardTotal += u.total
            
        i += 1
    
    return decklists_modified

def top(render_params, data):
    render_params["body"] = data["body"]
    render_params["title"] = data["title"]
    
    return render_params

def dert(render_params, data):
    did = None
    if request.args.get("did") and request.args.get("did") != 'all':
        did = request.args.get("did")
    else:
        return None
    
    offset = 0
    per_page = 10

    if request.args.get("page"):
        if int(request.args.get("page")) > 1:
            offset = per_page * int(request.args.get("page"))
    href = "?act=dert&did=" + did + "&page={0}"
    
    decklists = None
    decklists = Decklist.getDecklistByDecklistId(did, offset, per_page)
    
    deck_title = Decklist.getDeckNameByDid(did)
    deck_title = deck_title[0].name
    
    decklists_modified = processDecklists(decklists)

    #検�結果合計    
    decklists_all = Decklist.getDecklistByDecklistId(did, None, None)
    amount_by_date = Decklist.getDecklistAmountByDecklistId(did)
    
    total_users = []
    for u in decklists_all:
        if u.player_name not in total_users:
            total_users.append(u.player_name)
    
    total = len(total_users)
        
    today = date.today()
    year_ago = today - relativedelta(years=1)
    pagination = utils.pagination(total, deck_title, href, per_page)
    chart = lineChartCreate(Decklist.getDecklistAmountByDecklistId(did, year_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))
    
    top_cards_played_main = Decklist.getMtgCardUsageByMetaId(did, limit_by=12, where_board=1, from_date=year_ago.strftime('%Y-%m-%d'), to_date=today.strftime('%Y-%m-%d'))
    top_cards_played_side = Decklist.getMtgCardUsageByMetaId(did, limit_by=12, where_board=2, from_date=year_ago.strftime('%Y-%m-%d'), to_date=today.strftime('%Y-%m-%d'))
    
    render_params["conoha_url"]                 = config['CONOHA_STORAGE_CARDIMG_URL']
    render_params["per_page_skip"]              = per_page
    render_params["pagination"]                 = pagination
    render_params['deck_lists']                 = decklists_modified
    render_params['deck_title']                 = deck_title
    render_params['top_cards_played_main']      = top_cards_played_main
    render_params['top_cards_played_side']      = top_cards_played_side
    render_params["body"]                       = data["body"]
    render_params["title"]                      = data["title"]
    render_params["amount_by_date"]             = amount_by_date   
    render_params["include_css"]                = []
    render_params["include_js"]                 = []
    
    render_params["include_css"].append({'css': "amcharts/plugins/export/export.css"})
    render_params["include_js"].append({'js': "amcharts/amcharts.js"})
    render_params["include_js"].append({'js': "amcharts/plugins/export/export.min.js"})
    render_params["include_js"].append({'js': "amcharts/themes/none.js"})
    render_params['include_js'].append({'js': 'amcharts/serial.js'})
    render_params['include_js'].append({'js': 'amcharts/themes/light.js'})
    render_params['include_js'].append({'js': 'amcharts/plugins/dataloader/dataloader.min.js'})
    render_params["additional_scripts"] = [chart]
    
    render_params["include_js"].append({"js": "deckDetail.js"})
    render_params["include_css"].append({"css": "deckdetail.css"})
    
    if is_Smartphone() == False:
        render_params["include_css"].append({'css': "showCardDetails.css"})
        render_params["include_js"].append({"js": "showCardDetails.js"})
    
    return render_params