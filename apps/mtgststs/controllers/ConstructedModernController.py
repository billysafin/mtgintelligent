# -*- encoding:utf8 -*-
#from helpers.SerialChartCreater import emptySerialJs
import datetime
from dateutil.relativedelta import relativedelta
from flask import request
from helpers.PieChartCreater import createPieChart
from helpers.SerialChartCreater import createSerialChart
import services.MtgTournamentsService as TourAll
from Main import config

COUNTRY_ID = None

FROM_DATE = datetime.datetime.today() - relativedelta(years=1)
FROM_DATE = FROM_DATE.strftime('%Y-%m-%d')
#FROM_DATE = '2017-01-01'

TO_DATE = datetime.date.today().strftime('%Y-%m-%d')
FORMAT_NAME = 'modern'
FORMAT_ID = 2

def _returnRenders(render_params, data):
    render_params["body"] = data["body"]
    render_params["title"] = data["title"]
    render_params["include_js"] = [
        {'js': "amcharts/amcharts.js"},
        {'js': "amcharts/plugins/export/export.min.js"},
        {'js': "amcharts/themes/none.js"}
    ]
    render_params["include_css"] = [
        {'css': "amcharts/plugins/export/export.css"}
    ]
    
    return render_params

def _processTournaments(render_params, tournaments, format):
    tour = []
    for u in tournaments:
        tour.append({
            "id"       :u.id,
            "date"     :u.start,
            "name"     :u.name
        })
    render_params[format] = tour
    
    return render_params
    
def _getTopFiveDecks(from_date, to_date, format):
    tour_ids = TourAll.getTournaments(from_date, to_date, format, COUNTRY_ID, None)
    tournament_ids = []
    for i in tour_ids:
        tournament_ids.append(i.id)
        
    top_five = TourAll.getTopFiveDeckTypesByFormat(tournament_ids)
    
    tour = []
    total = 0
    for i in top_five:
        total += int(i.count)
    
    for u in top_five:
        percent = round((int(u.count) / int(total)) * 100)
        
        tour.append({
            'id'             : u.deck_id,
            'deck_name'      : u.name,
            'total_number'   : u.count,
            'total_percent'  : str(percent) + '%'
        })
        
    return tour

def top(render_params, data):
    result = TourAll.getTournaments(FROM_DATE, TO_DATE, FORMAT_ID, COUNTRY_ID, 10)
    render_params = _processTournaments(render_params, result, FORMAT_NAME)
    
    charts=[]
    chart = createPieChart(FROM_DATE, TO_DATE, FORMAT_NAME, FORMAT_ID, None, None, False, 5, None, None, None, None)
    
    charts.append(chart)
    
    topFive = _getTopFiveDecks(FROM_DATE, TO_DATE, FORMAT_ID)
    render_params['top_five'] = topFive
    
    render_params = _returnRenders(render_params, data)
    render_params['include_js'].append({'js': "amcharts/pie.js"})
    render_params["additional_scripts"] = charts
    render_params["include_css"].append({'css': "constructed.css"})
    
    return render_params

def stats(render_params, data):
    
    if request.form.get("fd"):
        from_date = request.form.get("fd")
    else:
        from_date = FROM_DATE
        
    if request.form.get("td"):
        to_date = request.form.get("td")
    else:
        to_date = TO_DATE
        
    if request.form.get("did") and request.form.get("did") != 'all':
        dids = request.form.get("did")
    else:
        dids = None
        
    if request.form.get("dmn"):
        deck_meta_names = request.form.get("dmn")
    else:
        deck_meta_names = None
        
    charts=[]
    click_event = []
    
    conoha_url = config['CONOHA_STORAGE_CARDIMG_URL']
    
    event = {}
  
    event['event'] = 'pullOutSlice'
    event['function'] = 'function(e){'
    
    event['function'] += 'if (pieDiv' + FORMAT_NAME + '.selectedIndex !== undefined){'
    event['function'] += 'pieDiv' + FORMAT_NAME + '.clickSlice(pieDiv' + FORMAT_NAME + '.selectedIndex);}'
    event['function'] += 'pieDiv' + FORMAT_NAME + '.selectedIndex = e.dataItem.index;'
    
    event['function'] += 'var dp = e.dataItem.dataContext;'
    event['function'] += 'var title = dp[pieDiv' + FORMAT_NAME + '.titleField];'
    event['function'] += 'var url = "/ajax/ajaxConstList";'
    event['function'] += 'var jObject = new Object();'    
    event['function'] += 'jObject["dmn"] = title;'
    event['function'] += 'jObject["format_id"] = ' + str(FORMAT_ID) + ';'
    event['function'] += 'var jString = JSON.stringify(jObject, null, "");'    
    event['function'] += '$.ajax({type:"POST",url:url,data:jString,'
    event['function'] += 'dataType:"json",contentType: "application/json",'
    event['function'] += 'success:function(_result){'
    event['function'] += 'var result=JSON.parse(_result);'
    event['function'] += 'if(result[0].error !== "error"){'
    
    event['function'] += 'var meta_name;'
    event['function'] += 'var player;'
    event['function'] += '$.each(result,function(index,val){'
    event['function'] += 'meta_name=val.meta_name;'
    event['function'] += 'player=val.player_name;'
    event['function'] += 'return false;'
    event['function'] += '});'
    event['function'] += 'var caption = "<center><b>" + meta_name + "</b><br /><span>" + player + "</span></center>";'
    event['function'] += 'var tbody="";'
    event['function'] += 'var lands="";'
    event['function'] += 'var creatures="";'
    event['function'] += 'var spells="";'
    event['function'] += 'var side="";'
    event['function'] += 'var popWindow="";'
    
    event['function'] += 'var landCount=0;'
    event['function'] += 'var creatureCount=0;'
    event['function'] += 'var spellCount=0;'
    event['function'] += 'var sideCount=0;'
    
    event['function'] += 'var conoha_url = "' + conoha_url + '";'
    event['function'] += 'var lang = "_" + "' + render_params['lang'] + '";'
    event['function'] += 'var newName="";'
    
    event['function'] += '$.each(result,function(index,val){'
    event['function'] += 'newName=conoha_url + val.image_name;'
    
    event['function'] += 'var cardname = val.card_name;'
    event['function'] += 'if(cardname == "" || typeof cardname == "undefined"){'
    event['function'] +=  'cardname = val.card_name_en;'
    event['function'] += '}'
    
    event['function'] += 'if(val.amount == undefined){'
    event['function'] += 'return true;'
    event['function'] += '}'
    
    event['function'] += 'if(typeof val.card_type == "undefined"){'
    event['function'] += 'return true;'
    event['function'] += '}'
    
    event['function'] += 'if(parseInt(val.board) != 1 && parseInt(val.board) == 2){'
    event['function'] += 'side += val.amount + " <a title=\'" + newName + "\' href=\'" + val.card_url + "\' target=\'_blank\' class=\'clickable showCard\'>" + cardname + "</a><br />";'
    event['function'] += 'sideCount += val.amount;'
    event['function'] += 'return true;'
    event['function'] += '}'
    event['function'] += 'if(val.card_type.match(/Land/)){'
    event['function'] += 'lands += val.amount + " <a title=\'" + newName + "\' href=\'" + val.card_url + "\' target=\'_blank\' class=\'clickable showCard\'>" + cardname + "</a><br />";'
    event['function'] += 'landCount += val.amount;'
    event['function'] += 'return true;'
    event['function'] += '}'
    event['function'] += 'if(val.card_type.match(/Creature/)){'
    event['function'] += 'creatures += val.amount + " <a title=\'" + newName + "\' href=\'" + val.card_url + "\' target=\'_blank\' class=\'clickable showCard\'>" + cardname + "</a><br />";'
    event['function'] += 'creatureCount += val.amount;'
    event['function'] += 'return true;'
    event['function'] += '}'
    event['function'] += 'spells += val.amount + " <a title=\'" + newName + "\' href=\'" + val.card_url + "\' target=\'_blank\' class=\'clickable showCard\'>" + cardname + "</a><br />";' 
    event['function'] += 'spellCount += val.amount;'
    event['function'] += '});'
    
    event['function'] += 'lands += "<hr style=\'margin:0em;margin-bottom:-1em;\' width=\'100%\' align=\'left\'><br />";';
    event['function'] += 'lands += "<p>Total:&nbsp;&nbsp;" + landCount + "&nbsp;&nbsp;Cards</p><br />";';
    event['function'] += 'creatures += "<hr style=\'margin:0em;margin-bottom:-1em;\' width=\'100%\' align=\'left\'><br />";';
    event['function'] += 'creatures += "<p>Total:&nbsp;&nbsp;" + creatureCount + "&nbsp;&nbsp;Cards</p><br />";';
    event['function'] += 'spells += "<hr style=\'margin:0em;margin-bottom:-1em;\' width=\'100%\' align=\'left\'><br />";';
    event['function'] += 'spells += "<p>Total:&nbsp;&nbsp;" + spellCount + "&nbsp;&nbsp;Cards</p><br />";';
    event['function'] += 'side += "<hr style=\'margin:0em;margin-bottom:-1em;\' width=\'100%\' align=\'left\'><br />";';
    event['function'] += 'side += "<p>Total:&nbsp;&nbsp;" + sideCount + "&nbsp;&nbsp;Cards</p><br />";';

    event['function'] += 'tbody += "<div class=\'col-xs-12 col-md-4 col-sm-4 ml-12\'>" + lands + "" + creatures + "</div>";'
    event['function'] += 'tbody += "<div class=\'col-xs-12 col-md-4 col-sm-4 ml-12\'>" + spells + "</div>"'
    event['function'] += '+ "<div class=\'col-xs-12 col-md-4 col-sm-4 ml-12\'>" + side + "</div>";'
    event['function'] += 'caption += tbody;'
    
    event['function'] += '$("#decklistTable").empty();'
    event['function'] += '$("#decklistTable").append(caption);'
    event['function'] += '$("#decklist").show("fast");'

    event['function'] += 'simple_tooltip("#decklistTable > div > a", "tooltip");'
    event['function'] += '}}});'
    event['function'] += '}'
    
    click_event.append(event)
    
    event_2 = {}
    event_2['event'] = 'pullInSlice'
    event_2['function'] = 'function(e){'
    event_2['function'] += 'var dpIn = e.dataItem.dataContext;'
    event_2['function'] += 'var titleIn = dpIn[pieDiv' + FORMAT_NAME + '.titleField];'
    event_2['function'] += 'var divTitle = $("#decklistTable > caption > center > b").text();'
    event_2['function'] += 'if(divTitle !== undefined && divTitle !== ""){'
    event_2['function'] += 'if(divTitle == titleIn){'
    event_2['function'] += 'delete pieDiv' + FORMAT_NAME + '.selectedIndex;'
    event_2['function'] += '$("#decklist").hide("fast");'
    event_2['function'] += '$("#decklistTable").empty();'
    event_2['function'] += '}}}'
    
    click_event.append(event_2)
    
    pieChartData = createPieChart(from_date, to_date, FORMAT_NAME, FORMAT_ID, None, None, None, 10, dids, deck_meta_names, click_event, True)
    pieChart = pieChartData['data']
    charts.append(pieChart)
    
    serialChart = createSerialChart(from_date, to_date, FORMAT_NAME, FORMAT_ID, None, None, None, 10, deck_meta_names, None)
    charts.append(serialChart)
    
    
    render_params = _returnRenders(render_params, data)
    render_params['include_js'].append({'js': 'amcharts/pie.js'})
    render_params['include_js'].append({'js': 'amcharts/serial.js'})
    render_params['include_js'].append({'js': 'amcharts/themes/light.js'})
    
    render_params['include_js'].append({'js': 'amcharts/plugins/dataloader/dataloader.min.js'})
    render_params['include_js'].append({'js': 'constructed-stats.js'})
    #render_params['include_js'].append({'js': 'showCardDetails.js'})
    #render_params['include_css'].append({'css': 'showCardDetails.css'})
    render_params["additional_scripts"] = charts
    render_params["include_css"].append({'css': "constructedStats.css"})
    
    return render_params