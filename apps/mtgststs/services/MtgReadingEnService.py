# -*- encoding:utf8 -*-
from models.MtgReadingEn import ArticlesEn
from models.SiteNames import Sites
from models.Country import Country
from services.ServiceManager import sql_logging

@sql_logging
def latest(limit_num):
    query = ArticlesEn.query.join(Sites, Sites.id == ArticlesEn.source_from)
    query = query.join(Country, Country.id == Sites.country_id)
    query = query.with_entities(ArticlesEn.published, ArticlesEn.title, ArticlesEn.link, ArticlesEn.date, Sites.site_name, Country.flag_prefix, Sites.image)
    query = query.filter_by(delete_flag=0).order_by(ArticlesEn.published.desc()).limit(limit_num)
    return query

#全ての記事
@sql_logging
def all_aticles():
    return ArticlesEn.query.filter_by(delete_flag=0).all()

#過去２５件づつ
@sql_logging
def past_25(offset):
    past_query = ArticlesEn.query
    past_query = past_query.join(Sites, Sites.id == ArticlesEn.source_from)
    past_query = past_query.with_entities(ArticlesEn.published, ArticlesEn.title, ArticlesEn.link, ArticlesEn.date, Sites.site_name, Country.flag_prefix, Sites.image)
    past_query = past_query.filter_by(delete_flag=0).order_by(ArticlesEn.published.desc())
    return past_query.offset(offset).limit(25)