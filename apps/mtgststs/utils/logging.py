# -*- encoding:utf8 -*-
from flask import request
from Main import utils, config
from geoip import geolite2
import logging

def geoip():
    geo = {}
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
        
    ip = ip.replace(" ", "")
    if ip is None or ip == "b''" or ip == '':
        #無理やり日本IP
        ip = config["JAPANESE_IP"]
        match = geolite2.lookup(config["JAPANESE_IP"])
    else:
        match = geolite2.lookup(ip)
    
    geo.update({"ip" : ip})
    geo.update({"match" : match})
    return geo

def access_logging(controller, action):
    ip = geoip()['ip']
    match = geoip()['match']
    access_logger = logging.getLogger('access_logger')
    headers = dict(request.headers)
    del headers['User-Agent']
    headers.update({
        "controller" : controller,
        "action" : action,
        "platform" : request.user_agent.platform,
        "browser" : request.user_agent.browser,
        "version" : request.user_agent.version,
        "language" : request.user_agent.language,
        "ua_string" : request.user_agent.string,
        "ip" : ip,
        "http_query" : request.query_string.decode('utf-8'),
        "scheme" : request.scheme,
        "url" : request.url,
        "cookie" : request.cookies,
        "country" : match.country,
        "continent" : match.continent,
        "timezone" : match.timezone
    })
    export_access = utils.generate_ltsv(headers)
    access_logger.info(export_access)

def crtitcal_logging(code, msg):
    ip = geoip()['ip']
    match = geoip()['match']
    headers = dict(request.headers)
    critical_logger = logging.getLogger('critical_logger')
    del headers['User-Agent']
    headers.update({
        "ip" : ip,
        "http_query" : request.query_string.decode('utf-8'),
        "scheme" : request.scheme,
        "url" : request.url,
        "cookie" : request.cookies,
        "country" : match.country,
        "continent" : match.continent,
        "timezone" : match.timezone,
        "error_code" : code,
        "error_message" : msg.strip()
    })
    export_critical = utils.generate_ltsv(headers)
    critical_logger.critical(export_critical)

def sql_logging():
    ip = geoip()['ip']
    match = geoip()['match']
    headers = dict(request.headers)
    del headers['User-Agent']
    sql_log = logging.getLogger('sqlalchemy.engine')
    headers.update({
        "ip" : ip,
        "http_query" : request.query_string.decode('utf-8'),
        "scheme" : request.scheme,
        "url" : request.url,
        "cookie" : request.cookies,
        "country" : match.country,
        "continent" : match.continent,
        "timezone" : match.timezone
    })
    export_sql = utils.generate_ltsv(headers)
    sql_log.info(export_sql)
    