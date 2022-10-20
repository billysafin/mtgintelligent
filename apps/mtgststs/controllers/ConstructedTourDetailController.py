# -*- encoding:utf8 -*-
from flask import request
import services.MtgDecklistService as Decklist
import re
from Main import config
import services.MtgTournamentsService as Tournaments

def _getTourdecklists(tour_id):
    decklistDetsils = Decklist.getDecklistByTourId(tour_id)
        
    return decklistDetsils

def _getDecklists(decklistDetsils):
    decklists          = []
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
    total_dict_count   = len(decklistDetsils)
    
    for u in decklistDetsils:
        if len(checked) > 0:
            if str(u.player_name) != checked['player_name'] or i == total_dict_count:
                decklists.append({
                    "player_name"  : checked['player_name']
                    ,"meta_name"   : checked['meta_name']
                    ,"rank"        : checked['rank']
                    ,"omwp"        : checked['omwp']
                    ,"gwp"         : checked['gwp']
                    ,"ogwp"        : checked['ogwp']      
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
            
        checked = {
            "player_name"  : str(u.player_name)
            ,"meta_name"   : str(u.meta_name)
            ,"rank"        : u.player_rank
            ,"omwp"        : u.player_omwp
            ,"gwp"         : u.player_gwp
            ,"ogwp"        : u.player_ogwp  
        }
                
        if int(u.which) is 1:
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
    
    return decklists

def _getTourDetails(tour_id):
    details = Tournaments.getTournamentById(tour_id)
    
    _tourDetails = []
    for u in details:
        _tourDetails .append({
          "start"     : str(u.MtgTournament.start)
          ,"end"      : str(u.MtgTournament.end)
          ,"location" : str(u.location)
          ,"name"     : str(u.MtgTournament.name)
          ,"rounds"   : u.MtgTournament.rounds
          ,"format"   : str(u.format_name)
          
        })
    
    return _tourDetails

def dert(render_params, data):
    if request.args.get("tour"):
        tour_id = request.args.get("tour")
    else:
        raise ErrorHandler(traceback.format_exc(), status_code = 404)
        
    decklistDetsils = _getTourdecklists(tour_id)
    decklists = _getDecklists(decklistDetsils)
    tourDetails = _getTourDetails(tour_id)
    
    render_params["conoha_url"]         = config['CONOHA_STORAGE_CARDIMG_URL']
    render_params["body"]               = data["body"]
    render_params["title"]              = data["title"]
    render_params["deck_lists"]         = decklists
    render_params["tour_details"]       = tourDetails
    
    render_params["include_js"] = [
        {"js": "tourDetail.js"}
        ,{"js": "showCardDetails.js", "param":"defer=defer"}
    ]
    render_params["include_css"] = [
        {'css': "showCardDetails.css"}
    ]
    
    return render_params