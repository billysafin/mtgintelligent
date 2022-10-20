# -*- encoding:utf8 -*-
from models.Country import Country
from services.ServiceManager import sql_logging

#全ての検索サイト
@sql_logging
def all_country():
    return Country.query.filter(Country.id != 1, Country.delete_flag == 0).all()