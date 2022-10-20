# -*- encoding:utf8 -*-
from models.MtgReadingEn import ArticlesEn
from models.MtgReadingJp import ArticlesJp
from models.SiteNames import Sites
from models.Country import Country
from services.ServiceManager import sql_logging
from sqlalchemy import *

#最新記事 各サイト１件のみ
@sql_logging
def latest_noduplicate(limit_num, offset_num):
    query1 = ArticlesJp.query.join(Sites, Sites.id == ArticlesJp.source_from)
    query1 = query1.join(Country, Country.id == Sites.country_id)
    query1 = query1.with_entities(ArticlesJp.published, ArticlesJp.title, ArticlesJp.link, ArticlesJp.date, Sites.site_name, Country.flag_prefix, Sites.image)
    query1 = query1.filter_by(delete_flag=0)

    query2 = ArticlesEn.query.join(Sites, Sites.id == ArticlesEn.source_from)
    query2 = query2.join(Country, Country.id == Sites.country_id)
    query2 = query2.with_entities(ArticlesEn.published, ArticlesEn.title, ArticlesEn.link, ArticlesEn.date, Sites.site_name, Country.flag_prefix, Sites.image) 
    query2 = query2.filter_by(delete_flag=0)

    return query1.union(query2).order_by(ArticlesJp.published.desc()).group_by(Sites.site_name).offset(offset_num).limit(limit_num)

#最新記事
@sql_logging
def latest(limit_num, offset_num):
    query1 = ArticlesJp.query.join(Sites, Sites.id == ArticlesJp.source_from)
    query1 = query1.join(Country, Country.id == Sites.country_id)
    query1 = query1.with_entities(ArticlesJp.published, ArticlesJp.title, ArticlesJp.link, ArticlesJp.date, Sites.site_name, Country.flag_prefix, Sites.image) 
    query1 = query1.filter_by(delete_flag=0)

    query2 = ArticlesEn.query.join(Sites, Sites.id == ArticlesEn.source_from)
    query2 = query2.join(Country, Country.id == Sites.country_id)
    query2 = query2.with_entities(ArticlesEn.published, ArticlesEn.title, ArticlesEn.link, ArticlesEn.date, Sites.site_name, Country.flag_prefix, Sites.image) 
    query2 = query2.filter_by(delete_flag=0)

    return query1.union(query2).order_by(ArticlesJp.published.desc()).offset(offset_num).limit(limit_num)

#全ての記事
@sql_logging
def all_aticles():
    query1 = ArticlesJp.query.filter_by(delete_flag=0)
    query2 = ArticlesEn.query.filter_by(delete_flag=0)
    return query1.union(query2).count()

#過去記事検索
@sql_logging
def search(langs, dates, sites, limit_num, offset_num):
    if langs == None and dates == None and sites == None:
        result = latest(limit_num, offset_num)
    else:
        #大元
        query1 = ArticlesJp.query.join(Sites, Sites.id == ArticlesJp.source_from)
        query1 = query1.join(Country, Country.id == Sites.country_id)
        query1 = query1.with_entities(ArticlesJp.published, ArticlesJp.title, ArticlesJp.link, ArticlesJp.date, Sites.id, Sites.site_name, Country.flag_prefix, Sites.image) 
        query1 = query1.filter_by(delete_flag=0)

        query2 = ArticlesEn.query.join(Sites, Sites.id == ArticlesEn.source_from)
        query2 = query2.join(Country, Country.id == Sites.country_id)
        query2 = query2.with_entities(ArticlesEn.published, ArticlesEn.title, ArticlesEn.link, ArticlesEn.date, Sites.id, Sites.site_name, Country.flag_prefix, Sites.image)
        query2 = query2.filter_by(delete_flag=0)
        query_final = query1.union(query2)

        #日付
        if 'date_from' in dates:
            query_final = query_final.filter(ArticlesJp.published >= dates['date_from'])
        if 'date_to' in dates:
            query_final = query_final.filter(ArticlesJp.published <= dates['date_to'])
        

        #言語選択
        if len(langs) == 1:
            query_final = query_final.filter(Country.id == langs[0])
        elif len(langs) > 1:
            query_final = query_final.filter(or_(*[Country.id == lang for lang in langs]))

        #サイト
        if len(sites) == 1:
            query_final = query_final.filter(Sites.id == sites[0])
        elif len(sites) > 1:
            query_final = query_final.filter(or_(*[Sites.id == site for site in sites]))

        total_q = query_final
        total = total_q.count()

        result = query_final.order_by(ArticlesJp.published.desc()).offset(offset_num).limit(limit_num)
    
        return_dic = {}
        return_dic['result'] = result
        return_dic['count'] = total
    return return_dic