from flask import request
from flask_paginate import Pagination

#flask-pagination
def pagination(total, record_name, href, per_page):
    search = False
    if request.args.get('q'):
        search = True
    page = request.args.get('page', type=int, default=1)
    offset = (page - 1) * per_page
        
    paginate = Pagination(per_page=per_page, offset=offset, page=page, total=total - per_page, search=search, record_name=record_name, href=href, inner_window=1, outer_window=0, css_framework='bootstrap3')
    return paginate

#ltsv化
def generate_ltsv(kv_dic):
    ltsv = ''
    for key, value in kv_dic.items():
        ltsv += '{0}:{1}\t'.format(key, value)
    return ltsv
