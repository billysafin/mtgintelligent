# -*- encoding:utf8 -*-
from Main import config, log
from flask import request
import re

geo_accept = config['GEO_ACCEPT']

#sqlログ
def sql_logging(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        log.sql_logging()
        return func(*args,**kwargs)
    return wrapper

def geoCheck():
    lang_cookie = request.cookies.get('lang', None)
    language = re.sub('/', '', request.path[0:3])
    
    if language == 'aj':
        if lang_cookie is not None and lang_cookie != '':
            language = lang_cookie
        else:
            UA_langs = request.accept_languages
            for lang in UA_langs:
                ua_lang  = re.sub(r'-.*$', '', re.sub(r';.*$', '', lang[0]))
                if geo_accept[ua_lang] == "True":
                    language = ua_lang
                    break
    else:
        UA_langs = request.accept_languages
        for lang in UA_langs:
            ua_lang  = re.sub(r'-.*$', '', re.sub(r';.*$', '', lang[0]))
            if geo_accept[ua_lang] == "True":
                language = ua_lang
                break
    
    if geo_accept[language] == "True":
        if lang_cookie != language:
            language = language
        else:
            language = lang_cookie
    else:        
        UA_langs = request.accept_languages
        for lang in UA_langs:
            ua_lang  = re.sub(r'-.*$', '', re.sub(r';.*$', '', lang[0]))
            if geo_accept[ua_lang] == "True":
                language = ua_lang
                break

    return language