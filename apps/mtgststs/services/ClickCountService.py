# -*- encoding:utf8 -*-
from models.ClickCount import ClickCount
from services.ServiceManager import sql_logging
from models.ModelManager import DB

@sql_logging
def insert_update_counter(post_type, post_href):
    result = ClickCount.query.filter(ClickCount.delete_flag == 0, ClickCount.type == post_type, ClickCount.href == str(post_href)).first()
    if result == None:
        counter = ClickCount(id = False, href = post_href, type = post_type, count = 1, delete_flag = 0)
        DB.session.add(counter)
        DB.session.commit()
    elif int(result.count) >= 1:
        result.count = int(result.count) + 1
        DB.session.commit()