# -*- encoding:utf8 -*-
from models.SiteNames import Sites
from services.ServiceManager import sql_logging

#全ての検索サイト
@sql_logging
def all_sites():
    return Sites.query.with_entities(Sites.id, Sites.country_id, Sites.site_name).filter_by(delete_flag=0).order_by(Sites.country_id.desc()).all()

#言語別
@sql_logging
def all_sites_by_lang(lang):
    query = Sites.query.with_entities(Sites.id, Sites.top_link, Sites.site_name, Sites.country_id)
    query = query.filter_by(delete_flag=0)
    query = query.filter_by(country_id=lang)
    query = query.order_by(Sites.id.desc())
    query = query.all()
    
    return query