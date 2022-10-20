# -*- encoding:utf8 -*-
import services.MtgTournamentsService as TourAll
from helpers.CommonHelper import generate_random_color

COUNTRY_ID = None

def createPieChart(from_date, to_date, format_name, format_id, chart_limit, tour_limit, is_all, top_num, dids, deck_meta_names, click_event, isSync):
    tournament_ids = []
    
    if dids is not None:
        tournament_ids = dids
    else:
        tour_ids = TourAll.getTournaments(from_date, to_date, format_id, COUNTRY_ID, tour_limit)

        for i in tour_ids:
            tournament_ids.append(i.id)

    decktypes = TourAll.getDeckTypeByFormat(tournament_ids, chart_limit, deck_meta_names)
    
    chart_data = 'var pieDiv' + format_name + ' = '
    chart_data += 'AmCharts.makeChart("pieDiv' + format_name + '",' 
    chart_data += '{"type":"pie","theme":"none","colorField":"color"'
    chart_data += ',"labelColorField":"color","dataProvider":['

    mid = []
    
    if is_all is True:
        for u in decktypes:
            if u.name is not None or u.name is not '':
                chart_mid = '{"name":"' + str(u.name).replace('"', '').replace('\r\n','').replace('\r','').replace('\n','') + '",'
                chart_mid += '"count":"' + str(u.count) + '",'
                chart_mid += '"color":"' + generate_random_color() + '"}'
                mid.append(chart_mid)
    else:
        i = 1
        total_types = len(decktypes)
        other = 0
        
        for u in decktypes:
            if i <= top_num:
                if u.name is not None or u.name is not '':
                    chart_mid = '{"name":"' + str(u.name).replace('"', '').replace('\r\n','').replace('\r','').replace('\n','')  + '",'
                    chart_mid += '"count":"' + str(u.count) + '",'
                    chart_mid += '"color":"' + generate_random_color() + '"}'
                    mid.append(chart_mid)
            elif i == total_types:
                chart_mid = '{"name":"other",'
                chart_mid += '"count":"' + str(other) + '",'
                chart_mid += '"color":"' + generate_random_color() + '"}'
                mid.append(chart_mid)
            else:
                other += int(u.count)
            
            i += 1;
            
    chart_data += ','.join(mid)
    chart_data += '],"valueField":"count","titleField":"name","ballon":'
    chart_data += '{"fixedPosition":true},"export":{"enable":false}'
    chart_data += ',"listeners":['
    
    if click_event is not None:
        listLen = len(click_event)
        if listLen > 1:
            i = 1
            for item in click_event:
                chart_data += '{"event":"' + item['event'] + '",'
                chart_data += '"method":' + item['function'] + '}'
                
                if i is not listLen:
                    chart_data += ','
                    
                i += 1;
        else:
            chart_data += '{"event":"' + click_event[0]['event'] + '",'
            chart_data += '"method":' + click_event[0]['function'] + '}'
        chart_data += ']});'
    else:
        chart_data += ']});'

    if isSync is not None:
        return {"data": chart_data, "provider": mid}
    else:
        return chart_data

