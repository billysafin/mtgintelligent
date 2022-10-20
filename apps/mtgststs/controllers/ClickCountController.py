# -*- encoding:utf8 -*-
import services.ClickCountService as CC
from flask import request


def click_count_up():
    href = request.form.get('href')
    type = request.form.get('type')
    CC.insert_update_counter(type, href)