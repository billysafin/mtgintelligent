# -*- encoding:utf8 -*-
import datetime
from dateutil.relativedelta import relativedelta
import services.MtgTournamentsService as TourAll
import services.MtgReadingAllService as ReadingAll
import services.SitesService as Sites
import services.CountryService as Country
from Main import utils
from flask import request

COUNTRY_ID = None
LIMIT_NUM  = 5

FROM_DATE = datetime.datetime.today() + relativedelta(months=-6)
FROM_DATE = FROM_DATE.strftime('%Y-%m-%d')

TO_DATE = datetime.date.today().strftime('%Y-%m-%d')

ALL_FORMAT = {
    'standard'  : 1,
    'modern'    : 2,
    'legacy'    : 3,
    'vintage'   : 4
}

def _returnRenders(render_params, data):
    render_params["body"] = data["body"]
    render_params["title"] = data["title"]
    render_params["include_js"] = [
        {'js': "amcharts/amcharts.js"},
        {'js': "amcharts/pie.js"},
        {'js': "amcharts/plugins/export/export.min.js"},
        {'js': "amcharts/themes/none.js"}
    ]
    render_params["include_css"] = [
        {'css': "constructed.css"},
        {'css': "amcharts/plugins/export/export.css"}
    ]
    
    return render_params

def _createChart(from_date, to_date, format_name, format_id, chart_limit, tour_limit, is_all, top_num):
    tournament_ids = []
    tour_ids = TourAll.getTournaments(from_date, to_date, format_id, COUNTRY_ID, tour_limit)

    for i in tour_ids:
        tournament_ids.append(i.id)

    decktypes = TourAll.getDeckTypeByFormat(tournament_ids, chart_limit, None)
    
    chart_data = 'var chartDiv' + format_name + ' = '
    chart_data += 'AmCharts.makeChart("chartDiv' + format_name + '",' 
    chart_data += '{"type":"pie","theme":"none","dataProvider":['

    mid = []
    
    if is_all is True:
        for u in decktypes:
            chart_mid = '{"name":"' + str(u.name) + '",'
            chart_mid += '"count":"' + str(u.count) + '"}'
            mid.append(chart_mid)
    else:
        i = 1
        total_types = len(decktypes)
        other = 0
        for u in decktypes:
            if i <= top_num:
                chart_mid = '{"name":"' + str(u.name) + '",'
                chart_mid += '"count":"' + str(u.count) + '"}'
                mid.append(chart_mid)
            elif i == total_types:
                chart_mid = '{"name":"other",'
                chart_mid += '"count":"' + str(other) + '"}'
                mid.append(chart_mid)
            else:
                other += int(u.count)
            
            i += 1;
            

    mid_string = ','.join(mid)

    chart_data += mid_string
    chart_data += '],"valueField":"count","titleField":"name","ballon":'
    chart_data += '{"fixedPosition":true},"export":{"enable":true}});'

    return chart_data

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


def top(render_params, data):
    charts = []
    for format, value in ALL_FORMAT.items():
        result = TourAll.getTournaments(FROM_DATE, TO_DATE, value, COUNTRY_ID, LIMIT_NUM)
        render_params = _processTournaments(render_params, result, format)
        
        chart_data = _createChart(FROM_DATE, TO_DATE, format, value, None, None, False, 5)        
        charts.append(chart_data)
        
    render_params["additional_scripts"] = charts
    render_params = _returnRenders(render_params, data)
    
    return render_params

def articles(render_params, data):
    offset = 0

    if request.form.get("view_per_page_selected"):
        per_page = int(request.form.get("view_per_page_selected"))
    else:
        per_page = 25

    if request.args.get("page"):
        if int(request.args.get("page")) > 1:
            offset = per_page * int(request.args.get("page"))

    #全記事合計
    total = ReadingAll.all_aticles()

    #検索用 サイト
    sites = []
    sites_result = Sites.all_sites()
    for u in sites_result:
        sites.append({
            "id"            : u.id,
            "name"          : u.site_name,
            "country_id"    : u.country_id
        })
    #検索用 言�
    langs = []
    langs_result = Country.all_country()
    for u in langs_result:
        langs.append({
            "id"    : u.id,
            "name"  : u.name_en
        })

    #検索分岐
    news = []
    from pprint import pprint
    if request.args.get("sub"):
        #言語
        lang_query = []
        if request.form.getlist("lang"):
            lang_query = request.form.getlist("lang")
        #date
        date_query = {}
        if request.form.get("date_from"):
            date_query["date_from"] = request.form.get("date_from")
        if request.form.get("date_to"):
            date_query["date_to"] = request.form.get("date_to")

        #site
        sites_query = []
        if request.form.getlist("sites"):
            sites_query = request.form.getlist("sites")

        past = ReadingAll.search(lang_query, date_query, sites_query, per_page, offset)
        past = past['result']
        total = past['result']
    else:
        #全言語
        past = ReadingAll.latest(per_page, offset)

    for u in past:
        news.append({
            "prefix"        : u.prefix,
            "published"     : u.published,
            "title"         : u.title,
            "link"          : u.link,
            "date"          : u.date,
            "source_from"   : u.site_name
        })

    render_params["langs"]              = langs
    render_params["sites"]              = sites
    render_params["total_articles"]     = total
    render_params["news"]               = news
    render_params["per_page_skip"]      = offset
    render_params["pagination"]         = utils.pagination(total, "MTG記事", "?act=past_list&page={0}", per_page)
    render_params["pagination_items"]   = news
    render_params["body"]               = data["body"]
    render_params["title"]              = data["title"]
    render_params["include_css"]        = [
        {'css': "pagination.css"},
        {'css': "jquery-ui.theme.min.css"},
        {'css': "general-articles-past.css"}
    ]
    render_params["include_js"] = [
        {'js': "date-picker.js"},
        {'js': "lang-sites-search.js"}
    ]
    return render_params