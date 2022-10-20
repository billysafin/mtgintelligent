# -*- encoding:utf8 -*-
# 必要なライブラリをインポートする
from Main import app, log, config
from flask import request, render_template, send_from_directory, jsonify,redirect, make_response
from flask import redirect
import traceback, json, os, importlib
import services.CountryService as Country
import services.SitesService as Sites
import services.MtgTournamentsService as Tour
import re

geo_accept = config['GEO_ACCEPT']

def all_article_sites():
    return_values = {}
    langs_result = Country.all_country()
    for u in langs_result:
        values = Sites.all_sites_by_lang(u.id)
        return_values[u.prefix] = []
        if values is not None:
            for x in values:
                return_values[u.prefix].append({
                    'id'         : x.id,
                    'site_name'  : x.site_name,
                    'country_id' : x.country_id
                })
    return return_values
    
def latest_tours():
    retun_values = []
    tours = Tour.getLatestTours(None)
    for u in tours:
        if u.format_name is not 'Limited' and u.format_name is not 'Other':
            format = 'constructed'
        else:
            format = 'limited'
        retun_values.append({
            'id'     : u.id,
            'name'   : u.name,
            'format' : format
        })
    
    return retun_values
    

def geo_switch(language):
    result = {}  
    if language is not None:
        lang = language.upper()
    else:
        lang = 'JA'
    
    #html出力用
    f = open(os.path.dirname(__file__) + '/../i18n/' + lang + '/view_text.json' ,'r')
    data = json.load(f)
    result.update({'data' : data})
    f.close()
    
    result.update({
        'render_common' : {
            'meta'              : data['meta'],
            'menus'             : data['menus'],
            'sub_menus'         : data['sub_menus'],
            'titles'            : data['titles'],
            'lang'              : lang.lower(),
            'langs'             : geo_accept.keys(),
            'footer'            : data['footer'],
            'header'            : data['header'],
            'side_menu'         : data['side_menu'],
            'all_article_sites' : all_article_sites(),
            'latest_five_tours' : latest_tours()
        }
    })
    return result

#全エラーを処理
class ErrorHandler(Exception):
    status_code = 500

    def __init__(self, message, status_code = None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            error_type_accept = config['errors']
            if str(status_code) in error_type_accept.keys():
                if error_type_accept[str(status_code)] == 'True':
                    self.status_code = status_code
                    
    def error_process(self):
        result = geo_switch(None)
        render_common = result['render_common']
        data = result['data']
        log.access_logging(self.status_code, self.status_code)
        log.crtitcal_logging(self.status_code, self.message)
        controller = importlib.import_module('controllers.errors.' +  str(self.status_code) + 'Controller')
        action = getattr(controller, 'error' + str(self.status_code))
        return action(render_common, data[str(self.status_code)])

    def code(self):
        return int(self.status_code)

#全error
@app.errorhandler(ErrorHandler)
def error(error):
    params = error.error_process()
    return render_template(str(error.status_code) + '.html', **params), error.status_code

#controller/action処理
class ControllerActionName:
    def __init__(self, params):
        self.tmp = None
        if isinstance(params, list) or isinstance(params, dict):
            self.tmp = ' '.join(params)
        else:
            self.tmp = params
    def cap_name(self):
        return self.tmp.title().replace(' ', '')

#favicon対応
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/favicon.ico')

#robots.txt
@app.route('/robots.txt')
def robot():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robot.txt')

#ドメインのみでのアクセス用
@app.route('/', methods=['GET', 'POST'])
def index():
    #言語
    lang_cookie = request.cookies.get('lang', None)
    language = 'ja'
    if lang_cookie is not None:
        if geo_accept[lang_cookie] == 'True':
            language = lang_cookie
    else:
        UA_langs = request.accept_languages
        for lang in UA_langs:
            ua_lang  = re.sub(r'-.*$', '', re.sub(r';.*$', '', lang[0]))
            if geo_accept[ua_lang] == 'True':
                language = ua_lang
                break
                
    return redirect('https://www.mtgstatistics.com/' + language + '/')

#click count用
@app.route('/click_count', methods=['POST'])
def click_count():
    controller = importlib.import_module('controllers.ClickCountController')
    action = getattr(controller, 'click_count_up')
    action()
    return jsonify(result=True)

#ajax用
@app.route('/ajax/<path:path>', methods=['POST'])
def ajax(path):
    controller = importlib.import_module('controllers.AjaxController')
    #url
    path_info = path.split('/')
    
    #errorかfaviconでない
    if path_info[0] is not 'favicon.ico' and str(path_info[0]) in config['errors'].keys():
        raise ErrorHandler('Bad Access ajax 1', code = int(path_info[0]))
    
    if len(path_info) == 1 and path_info[0] is not None:
        con_name = path_info[0]
    else:
        raise ErrorHandler(path_info[0], status_code = 404)
    
    action = getattr(controller, con_name)
    result = action()
    return jsonify(result)

#指定がある場合(例:/jp/index)
@app.route('/<path:path>', methods=['GET', 'POST'])
def router(path):
    #url���解
    path_info = path.split('/')

    #errorかfaviconでない
    if path_info[0] is not 'favicon.ico' and str(path_info[0]) in config['errors'].keys():
        raise ErrorHandler('Bad Access', code = int(path_info[0]))
    
    #言語
    lang_cookie = request.cookies.get('lang', None)
    language = 'ja'
    if lang_cookie is not None:
        if geo_accept[lang_cookie] == 'True':
            if path_info[0] != lang_cookie:
                language = path_info[0]
            else:
                language = lang_cookie
    else:
        UA_langs = request.accept_languages
        for lang in UA_langs:
            ua_lang  = re.sub(r'-.*$', '', re.sub(r';.*$', '', lang[0]))
            if geo_accept[ua_lang] == 'True':
                language = ua_lang
                break
        
    #2階層以上深くなることはしない
    con_name = 'index'
    if len(path_info) == 2 or (len(path_info) == 3 and path_info[2] is not None):
        if not path_info[1]:
            con_name = 'index'
        else:
            con_name = path_info[1]
    elif len(path_info) == 1:
        language = path_info[0]
        con_name = 'index'

    geo_switched = geo_switch(language)
    
    render_common = geo_switched['render_common']
    data = geo_switched['data']

    #controller/action
    if '_' in con_name:
        i18n = con_name
        splited = ControllerActionName(con_name.split('_'))
    elif con_name is not None:
        i18n = con_name
        splited = ControllerActionName(con_name)
    else:
        i18n = 'index'
        splited = ControllerActionName('index')
    name = splited.cap_name() + 'Controller'
    try:
        controller = importlib.import_module('controllers.' + name)
    except:
        raise ErrorHandler(traceback.format_exc(), status_code = 404)
    if not request.args.get('act'):
        query = request.query_string.decode('utf-8')
        if len(query) is not 0:
            raise ErrorHandler(traceback.format_exc(), status_code = 404)
        try:
            action = getattr(controller, 'top')
            params = action(render_common, data[str(i18n)])
            temp = splited.cap_name() + '.html'
        except:
            raise ErrorHandler(traceback.format_exc(), status_code = 404)
        action_name = 'top'
    else:
        try:
            action = getattr(controller, request.args.get('act').lower())
            params = action(render_common, data[str(i18n)])
            splited_action = ControllerActionName(request.args.get('act').split('_'))
            temp = splited.cap_name() + splited_action.cap_name() + '.html'
        except:
            raise ErrorHandler(traceback.format_exc(), status_code = 404)
        action_name = splited_action.cap_name()
    log.access_logging(name, action_name)
    
    response = make_response(render_template(temp, **params))
    response.set_cookie('lang', language)
    
    return response