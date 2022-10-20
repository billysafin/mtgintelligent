# -*- encoding:utf8 -*-
import json
import services.MtgTournamentsService as TourAll
from helpers.CommonHelper import generate_random_color

temp_data_provider = {}
COUNTRY_ID = None

def createvalueAxes():
    valueAxes = '{"id": "v1","axisAlpha": 0}, {'
    valueAxes += '"id": "v2","axisAlpha": 0,"position": "bottom",'
    valueAxes += '"type": "date"}'
    
    return valueAxes
        
def createGrphs(colors, meta_names):
    iTotal = len(colors)
    graphs = []
    i = 0
    
    while i < iTotal:
        values = '{"id":"' + meta_names[i] + '","bullet": "round","bulletBorderAlpha": 1,'
        values += '"bulletColor": "' + colors[i] + '","bulletSize": 5,"hideBulletsCount": 50,'
        values += '"lineThickness": 2,"title": "' + meta_names[i] + '"'
        values += ',"useLineColorForBulletBorder": true,'
        values += '"valueField": "' + meta_names[i] + '"'
        values += '}'
        #values += '"balloon":{"drop":true,"adjustBorderColor":false,'"color":"' + colors[i] + '"},'
        #values += ',"balloonText": "<span style=\'font-size:18px;\'>' + meta_names[i] + '<br>[[' + meta_names[i] + ']]</span>"}'
        
        graphs.append(values)
        i += 1
    
    return ','.join(graphs)

def createPreDataProvider(u):
    if str(u.start) not in temp_data_provider:
        temp_data_provider[str(u.start)] = '"' + str(u.name) + '":"' + str(u.count) + '"'
    else:
        temp_data_provider[str(u.start)] += ',"'  + str(u.name) + '":"' + str(u.count) + '"'

def createFinalDataProvider():
    data = ''
    
    i = 0;
    for u in sorted(temp_data_provider):
        
        
        if i == 0:
            data += '{'
            i += 1;
        else:
            data += ',{'
        
        data += '"date":"' + u + '",'
        data += temp_data_provider[u]
        data += '}'
    
    return data

def createSerialChart(from_date, to_date, format_name, format_id, chart_limit, tour_limit, is_all, top_num, deck_meta_names, dataProviderSync):
    tournament_ids = []
    tour_ids = TourAll.getTournaments(from_date, to_date, format_id, COUNTRY_ID, tour_limit)
    
    chart_data = 'var serialDiv' + format_name + ' = '
    chart_data += 'AmCharts.makeChart("serialDiv' + format_name + '",{"type":"serial",'
    chart_data += '"marginRight": 40,"marginLeft": 40,"autoMarginOffset": 20,'
    chart_data += '"mouseWheelZoomEnabled":true,"dataDateFormat": "YYYY-MM-DD",'
    chart_data += '"export":{"enabled":false},"balloon":{"borderThickness": 1,'
    chart_data += '"shadowAlpha": 0},"categoryField": "date","categoryAxis": {'
    chart_data += '"parseDates": true,"dashLength": 1,"minorGridEnabled": true},'
    chart_data += '"valueScrollbar":{"oppositeAxis":false,"offset":50,'
    chart_data += '"scrollbarHeight":10},"legend":{"useGraphSettings":true},'
    chart_data += '"synchronizeGrid":true,"chartScrollbar": {},"chartCursor":{"cursorPosition":"mouse"},'
    
    dataProvider = ''
    graphs = ''
    valueAxes = ''
    colors = []
    meta_names = []
    
    if dataProviderSync is not None:
        jsonObject = json.loads('[' + ','.join(dataProviderSync) + ']')
        
        for dicit in jsonObject:
            colors.append(dicit['color'])
            meta_names.append(dicit['name'])
            usages = TourAll.getDeckUsageBYDateMetaName(dicit['name'], from_date, to_date, None)
            createPreDataProvider(usages)
    else:
        for i in tour_ids:
            tournament_ids.append(i.id)

        decktypes = TourAll.getDeckTypeByFormat(tournament_ids, chart_limit, deck_meta_names)

        deck_ids = []
        if is_all is True:
            for u in decktypes:
                meta_names.append(u.name)
                colors.append(generate_random_color())
                
                deck_ids.append(u.deck_id)
                
            usages = TourAll.getDeckUsageBYDateMetaNameIdInClause(map(str,deck_ids), from_date, to_date)
            for usage in usages:
                createPreDataProvider(usage)
        else:
            i = 1
            for u in decktypes:
                if i <= top_num:
                    meta_names.append(u.name)
                    colors.append(generate_random_color())
                    deck_ids.append(u.deck_id)
                else:
                    break
                i += 1
                
            usages = TourAll.getDeckUsageBYDateMetaNameIdInClause(map(str,deck_ids), from_date, to_date)
                
            for usage in usages:   
                createPreDataProvider(usage)
                    
    graphs += '"graphs": ['
    graphs += createGrphs(colors, meta_names)
    graphs += '],'

    valueAxes = '"valueAxes":['
    valueAxes += createvalueAxes()
    valueAxes += '],'
    
    dataProvider += '"dataProvider":['
    dataProvider += createFinalDataProvider()
    dataProvider += ']'
    
    chart_data += graphs
    chart_data += valueAxes
    chart_data += dataProvider
    
    chart_data += '});'
  
    return chart_data

    return js