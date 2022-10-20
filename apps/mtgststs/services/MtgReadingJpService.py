# -*- encoding:utf8 -*-
from models.MtgReadingJp import ArticlesJp
from models.SiteNames import Sites
from models.Country import Country
from services.ServiceManager import sql_logging

#最新１０件
@sql_logging
def latest(limit_num):
    query = ArticlesJp.query.join(Sites, Sites.id == ArticlesJp.source_from)
    query = query.join(Country, Country.id == Sites.country_id)
    query = query.with_entities(ArticlesJp.published, ArticlesJp.title, ArticlesJp.link, ArticlesJp.date, Sites.site_name, Country.flag_prefix, Sites.image)    
    return query.filter_by(delete_flag=0).order_by(ArticlesJp.published.desc()).limit(limit_num)

#全ての記事
@sql_logging
def all_aticles():
    return ArticlesJp.query.filter_by(delete_flag=0).all()

#過去２５件づつ
@sql_logging
def past_25(offset):
    past_query = ArticlesJp.query
    past_query = past_query.join(Sites, Sites.id == ArticlesJp.source_from)
    past_query = past_query.with_entities(ArticlesJp.published, ArticlesJp.title, ArticlesJp.link, ArticlesJp.date, Sites.site_name, Country.flag_prefix, Sites.image)
    past_query = past_query.filter_by(delete_flag=0).order_by(ArticlesJp.published.desc())
    return past_query.offset(offset).limit(25)