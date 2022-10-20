# -*- encoding:utf8 -*-
from Main import utils
from flask import request
import services.MtgTournamentsService as TourAll
import re

COUNTRY_ID = None

def _getAllTours(format, limit, offset):
    tour = TourAll.getAllTournaments(format, COUNTRY_ID, limit, offset)
    return tour

def listToStringForSql(keyword):
    return '"' + keyword + '"'

def top(render_params, data):
    render_params = const(render_params, data)
    
    return render_params

def allsearch(render_params, data):
    format_type = None
    per_page = 25
    ftype = ''
    offset = None
    
    #per_page
    if request.method == 'POST':
        if request.form.get("for") is not None and request.form.get("for") != '':
            format_type = request.form.get("for")
            ftype = '&for=' + request.form.get("for")
            
        if request.form.get("view_per_page_selected") is not None and request.form.get("view_per_page_selected") != '':
            per_page = int(request.form.get("view_per_page_selected"))
            
        if request.form.get("page") is not None and request.form.get("page") != '':
            offset = per_page * int(request.form.get("page"))
    elif request.method == 'GET':
        if request.args.get("for") is not None or request.args.get("for") != '':
            format_type = request.args.get("for")
            ftype = '&for=' + request.args.get("for")
        
        if request.args.get("view_per_page_selected") is not None and request.args.get("view_per_page_selected") != '':
            per_page = int(request.args.get("view_per_page_selected"))
            
        if request.args.get("page") is not None and request.args.get("page") != '':
            offset = per_page * int(request.args.get("page"))
    
    #date
    f = ''
    t = ''
    date_from = None
    date_to = None
    if request.form.get("date_from") and request.args.get("date_from") is None:
        date_from = request.form.get("date_from")
        f = "&f=" + request.form.get("date_from")
    elif request.form.get("f") and request.args.get("f") is None:
        date_from = request.form.get("f")
        f = "&f=" + request.form.get("f")
    elif request.form.get("date_from") is None and request.args.get("date_from"):
        date_from = request.args.get("date_from")
        f = "&f=" + request.args.get("date_from")
    elif request.form.get("f") is None and request.args.get("f"):
        date_from = request.args.get("f")
        f = "&f=" + request.args.get("f")    
        
    if request.form.get("date_to") and request.args.get("date_to") is None:
        date_to = request.form.get("date_to")
        t = "&t=" + request.form.get("date_to")
    elif request.form.get("t") and request.args.get("t") is None:
        date_to = request.form.get("t")
        t = "&t=" + request.form.get("t")
    elif request.form.get("date_to") is None and request.args.get("date_to"):
        date_to = request.args.get("date_to")
        t = "&t=" + request.args.get("date_to")
    elif request.form.get("t") is None and request.args.get("t"):
        date_to = request.args.get("t")
        t = "&t=" + request.args.get("t")
        
    #keywords
    kw = ''
    _query = None
    if request.method == 'POST':
        if request.form.get('tour_keywords'):
            kw = '&tour_keywords=' + request.form.get('tour_keywords')

            _query = re.sub(' {2,}', '\s', request.form.get('tour_keywords'))
            _query = re.sub('\s{2,}', '\s', _query)
            _query = _query.split()
            map(listToStringForSql, _query)
    elif request.method == 'GET':
        if request.args.get('tour_keywords'):
            kw = '&tour_keywords=' + request.args.get('tour_keywords')

            _query = re.sub(' {2,}', '\s', request.args.get('tour_keywords'))
            _query = re.sub('\s{2,}', '\s', _query)
            _query = _query.split()
            map(listToStringForSql, _query)
        
    result = TourAll.Search(format_type, COUNTRY_ID, per_page, _query, date_from, date_to, offset)
    total_count = TourAll.Search(format_type, COUNTRY_ID, None, _query, date_from, date_to, None)
    total = len(total_count)
    
    href = "?act=allsearch" + ftype + kw + "&page={0}"
    pagination = utils.pagination(total, "トーナメントリスト", href, per_page)
    
    tours_values = []
    for u in result:
        if u.format_name == 'Pauper' or u.format_name == 'Block' or u.format_name == 'Other':
            class_label = 'label label-danger'
            format = 'other'
        elif u.format_name == 'Standard':
            class_label = 'label label-default'
            format = 'standard'
        elif u.format_name == 'Modern':
            class_label = 'label label-primary'
            format = 'modern'
        elif u.format_name == 'Legacy':
            class_label = 'label label-success'
            format = 'legacy'
        elif u.format_name == 'Vintage':
            class_label = 'label label-info'
            format = 'vintage'
        elif u.format_name == 'Commander':
            class_label = 'label label-warning'
            format = 'commander'
        else:
            class_label = 'label label-danger'
            format = 'other'
            
        tours_values.append({
            "id"           : u.id,
            "name"         : u.name,
            "date"         : u.start,
            "class_label"  : class_label,
            "format"       : format
        })
        
    render_params['search'] = {
        "tour_keywords"           : request.form.get('tour_keywords')
        ,"date_from"              : date_from
        ,"date_to"                : date_to
        ,"view_per_page_selected" : "25"
        ,"format"                 : format_type
    }
    
    render_params["per_page_skip"]      = per_page
    render_params["pagination"]         = pagination
    render_params['list']               = tours_values
    render_params["body"]               = data["body"]
    render_params["title"]              = data["title"]
    render_params["include_css"]        = [
        {'css': "pagination.css"},
        {'css': "jquery-ui.theme.min.css"},
        {'css': "tournament_list.css"}
    ]
    render_params["include_js"] = [
        {'js': "date-picker.js"},
        {'js': "tournament-list.js"}
    ]
    return render_params

def allformat(render_params, data):
    per_page = 25
    tournament_list = _getAllTours(None, per_page, None)
    
    tours_values = []
    for u in tournament_list:
        if u.format_name == 'Pauper' or u.format_name == 'Block' or u.format_name == 'Other':
            class_label = 'label label-danger'
            format = 'other'
        elif u.format_name == 'Standard':
            class_label = 'label label-default'
            format = 'standard'
        elif u.format_name == 'Modern':
            class_label = 'label label-primary'
            format = 'modern'
        elif u.format_name == 'Legacy':
            class_label = 'label label-success'
            format = 'legacy'
        elif u.format_name == 'Vintage':
            class_label = 'label label-info'
            format = 'vintage'
        elif u.format_name == 'Commander':
            class_label = 'label label-warning'
            format = 'commander'
        else:
            class_label = 'label label-danger'
            format = 'other'
    
        tours_values.append({
            "id"           : u.id,
            "name"         : u.name,
            "date"         : u.start,
            "class_label"  : class_label,
            "format"       : format
        })
        
    allTour = _getAllTours(None, None, None)
    total = len(allTour)
    
    href = "?act=allformat&page={0}"
    pagination = utils.pagination(total, "トーナメントリスト", href, per_page)

    render_params['search'] = {
        "tour_keywords"          : "",
        "date_from"              : "",
        "date_to"                : "",
        "view_per_page_selected" : "25"
    }
    
    render_params["per_page_skip"]      = per_page
    render_params["pagination"]         = pagination
    render_params['list']               = tours_values
    render_params["body"]               = data["body"]
    render_params["title"]              = data["title"]
    render_params["include_css"]        = [
        {'css': "pagination.css"},
        {'css': "jquery-ui.theme.min.css"},
        {'css': "tournament_list.css"}
    ]
    render_params["include_js"] = [
        {'js': "date-picker.js"},
        {'js': "tournament-list.js"}
    ]
    return render_params

def const(render_params, data):
    offset = None
    per_page = 25
    
    if request.method == 'POST':
        if request.form.get("for"):
            format_type = request.form.get("for")
            
        if request.form.get("page") and int(request.form.get("page")) is not 1:
            offset = int(request.form.get("page")) * per_page
    elif request.method == 'GET':
        if request.args.get("for"):
            format_type = request.args.get("for")
            
        if request.args.get("page") and int(request.args.get("page")) is not 1:
            offset = int(request.args.get("page")) * per_page
    else:
        raise ErrorHandler(traceback.format_exc(), status_code = 404)
    
    tournament_list = _getAllTours(format_type, per_page, offset)
    tours_values = []
    for u in tournament_list:
        if u.format_name == 'Pauper' or u.format_name == 'Block' or u.format_name == 'Other':
            class_label = 'label label-danger'
            format = 'other'
        elif u.format_name == 'Standard':
            class_label = 'label label-default'
            format = 'standard'
        elif u.format_name == 'Modern':
            class_label = 'label label-primary'
            format = 'modern'
        elif u.format_name == 'Legacy':
            class_label = 'label label-success'
            format = 'legacy'
        elif u.format_name == 'Vintage':
            class_label = 'label label-info'
            format = 'vintage'
        elif u.format_name == 'Commander':
            class_label = 'label label-warning'
            format = 'commander'
        else:
            class_label = 'label label-danger'
            format = 'other'
    
        tours_values.append({
            "id"           : u.id,
            "name"         : u.name,
            "date"         : u.start,
            "class_label"  : class_label,
            "format"       : format
        })
        
    allTour = _getAllTours(format_type, None, None)
    total = len(allTour)
    
    href = "?act=allsearch&for=" + str(format_type) + "&page={0}"
    pagination = utils.pagination(total, "トーナメントリスト", href, per_page)

    render_params['search'] = {
        "tour_keywords"          : "",
        "date_from"              : "",
        "date_to"                : "",
        "view_per_page_selected" : "25",
        "format"                 : format_type
    }
    
    render_params["per_page_skip"]      = per_page
    render_params["pagination"]         = pagination
    render_params['list']               = tours_values
    render_params["body"]               = data["body"]
    render_params["title"]              = data["title"]
    render_params["include_css"]        = [
        {'css': "pagination.css"},
        {'css': "jquery-ui.theme.min.css"},
        {'css': "tournament_list.css"}
    ]
    render_params["include_js"] = [
        {'js': "date-picker.js"},
        {'js': "tournament-list.js"}
    ]
    return render_params

def search(render_params, data):
    #format
    ftype = ''
    format_type = None
    kw = ''
    _query = None
    
    if request.method == 'POST':
        if request.form.get("for"):
            format_type = request.form.get("for")
            ftype = '&for=' + request.form.get("for")
            
        if request.form.get('tour_keywords'):
            kw = '&tour_keywords=' + request.form.get('tour_keywords')

            _query = re.sub(' {2,}', '\s', request.form.get('tour_keywords'))
            _query = re.sub('\s{2,}', '\s', _query)
            _query = _query.split()
            map(listToStringForSql, _query)
    elif request.method == 'GET':
        if request.args.get("for"):
            format_type = request.args.get("for")
            ftype = '&for=' + request.args.get("for")
            
        if request.args.get('tour_keywords'):
            kw = '&tour_keywords=' + request.args.get('tour_keywords')

            _query = re.sub(' {2,}', '\s', request.args.get('tour_keywords'))
            _query = re.sub('\s{2,}', '\s', _query)
            _query = _query.split()
            map(listToStringForSql, _query)
    else:
        raise ErrorHandler(traceback.format_exc(), status_code = 404)
        
    #date
    date_query = {}
    f = ''
    t = ''
    date_from = None
    date_to = None
    if request.form.get("date_from") and request.args.get("date_from") is None:
        date_from = request.form.get("date_from")
        f = "&f=" + request.form.get("date_from")
    elif request.form.get("f") and request.args.get("f") is None:
        date_from = request.form.get("f")
        f = "&f=" + request.form.get("f")
    elif request.form.get("date_from") is None and request.args.get("date_from"):
        date_from = request.args.get("date_from")
        f = "&f=" + request.args.get("date_from")
    elif request.form.get("f") is None and request.args.get("f"):
        date_from = request.args.get("f")
        f = "&f=" + request.args.get("f")    
        
    if request.form.get("date_to") and request.args.get("date_to") is None:
        date_to = request.form.get("date_to")
        t = "&t=" + request.form.get("date_to")
    elif request.form.get("t") and request.args.get("t") is None:
        date_to = request.form.get("t")
        t = "&t=" + request.form.get("t")
    elif request.form.get("date_to") is None and request.args.get("date_to"):
        date_to = request.args.get("date_to")
        t = "&t=" + request.args.get("date_to")
    elif request.form.get("t") is None and request.args.get("t"):
        date_to = request.args.get("t")
        t = "&t=" + request.args.get("t")
        
    if request.form.get("view_per_page_selected"):
        per_page = int(request.form.get("view_per_page_selected"))
    else:
        per_page = 25
        
    offset = 0
    if request.method == 'POST':
        if request.form.get("page"):
            offset = per_page * int(request.form.get("page"))
    elif request.method == 'GET':
        if request.args.get("page"):
            offset = per_page * int(request.args.get("page"))
    
    result = TourAll.Search(format_type, COUNTRY_ID, per_page, _query, date_from, date_to,offset)
    total_count = TourAll.Search(format_type, COUNTRY_ID, None, _query, date_from, date_to, None)
    total = len(total_count)
    
    href = "?act=const"+ ftype + kw + f + t  + "&page={0}"
    pagination = utils.pagination(total, "トーナメントリスト", href, per_page)
    tours_values = []
    for u in result:
        if u.format_name == 'Pauper' or u.format_name == 'Block' or u.format_name == 'Other':
            class_label = 'label label-danger'
            format = 'other'
        elif u.format_name == 'Standard':
            class_label = 'label label-default'
            format = 'standard'
        elif u.format_name == 'Modern':
            class_label = 'label label-primary'
            format = 'modern'
        elif u.format_name == 'Legacy':
            class_label = 'label label-success'
            format = 'legacy'
        elif u.format_name == 'Vintage':
            class_label = 'label label-info'
            format = 'vintage'
        elif u.format_name == 'Commander':
            class_label = 'label label-warning'
            format = 'commander'
        else:
            class_label = 'label label-danger'
            format = 'other'
            
        tours_values.append({
            "id"           : u.id,
            "name"         : u.name,
            "date"         : u.start,
            "class_label"  : class_label,
            "format"       : format
        })
    
    
    render_params['search'] = {
        "tour_keywords"           : request.form.get('tour_keywords')
        ,"date_from"              : date_from
        ,"date_to"                : date_to
        ,"view_per_page_selected" : "25"
        ,"format"                 : format_type
    }
    
    render_params["per_page_skip"]      = per_page
    render_params["pagination"]         = pagination
    render_params['list']               = tours_values
    render_params["body"]               = data["body"]
    render_params["title"]              = data["title"]
    render_params["include_css"]        = [
        {'css': "pagination.css"},
        {'css': "jquery-ui.theme.min.css"},
        {'css': "tournament_list.css"}
    ]
    render_params["include_js"] = [
        {'js': "date-picker.js"},
        {'js': "tournament-list.js"}
    ]
    return render_params