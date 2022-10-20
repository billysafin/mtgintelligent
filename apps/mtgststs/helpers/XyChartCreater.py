# -*- encoding:utf8 -*-
import json
import services.MtgTournamentsService as TourAll
from helpers.CommonHelper import generate_random_color
import datetime

temp_data_provider = []
COUNTRY_ID = None
DATA_COUNT = None

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
        data_count = int(i) + 1
        
        values = '{"bullet":"round",'
        values += '"lineAlpha": 1,"lineColor":"' + colors[i] + '",'
        values += '"xField":"date' + str(data_count) + '","yFiled":"' + meta_names[i] + '"}'
        
        graphs.append(values)
        i += 1
    
    return ','.join(graphs)

def createPreDataProvider(usages, count):
    for u in usages:
        data = ''
        data += '{"date' + str(count) + '":"' + str(u.date) + '",'
        data += '"' + str(u.name) + '":' + str(u.count) + '}'
        
        temp_data_provider.append(data)

def createXyChart(from_date, to_date, format_name, format_id, chart_limit, tour_limit, is_all, top_num, deck_meta_names, dataProviderSync):
    tournament_ids = []
    tour_ids = TourAll.getTournaments(from_date, to_date, format_id, COUNTRY_ID, tour_limit)
    
    chart_data = 'var xyDiv' + format_name + ' = '
    chart_data += 'AmCharts.makeChart("xyDiv' + format_name + '",' 
    chart_data += '{"type":"xy","theme":"light","dataDateFormat": "YYYY-MM-DD",'
    chart_data += '"startDuration": 1.5,"chartCursor": {},'
    
    dataProvider = ''
    graphs = ''
    valueAxes = ''
    colors = []
    meta_names = []
    
    data_count = 1
    if dataProviderSync is not None:
        jsonObject = json.loads('[' + ','.join(dataProviderSync) + ']')
        
        for dicit in jsonObject:
            colors.append(dicit['color'])
            meta_names.append(dicit['name'])
            usages = TourAll.getDeckUsageBYDateMetaName(dicit['name'], from_date, to_date, None)
            createPreDataProvider(usages, data_count)
            data_count = data_count + 1
    else:
        for i in tour_ids:
            tournament_ids.append(i.id)

        decktypes = TourAll.getDeckTypeByFormat(tournament_ids, chart_limit, deck_meta_names)

        if is_all is True:
            for u in decktypes:
                meta_names.append(u.name)
                colors.append(generate_random_color())
                usages = TourAll.getDeckUsageBYDateMetaName(u.name, from_date, to_date, None)
                createPreDataProvider(usages, data_count)
                data_count = data_count + 1
        else:
            i = 1
            for u in decktypes:
                
                usages = TourAll.getDeckUsageBYDateMetaName(u.name, from_date, to_date, None)
                
                if i <= top_num:
                    meta_names.append(u.name)
                    colors.append(generate_random_color())
                    
                    createPreDataProvider(usages, data_count)
                    data_count = data_count + 1
                    
                i += 1
                
    graphs += '"graphs": ['
    graphs += createGrphs(colors, meta_names)
    graphs += '],'

    valueAxes = '"valueAxes":['
    valueAxes += createvalueAxes()
    valueAxes += '],'
    
    dataProvider += '"dataProvider":['
    dataProvider += ','.join(temp_data_provider)
    dataProvider += ']'
    
    chart_data += graphs
    chart_data += valueAxes
    chart_data += dataProvider
    
    chart_data += '});'
  
    return chart_data

    return js