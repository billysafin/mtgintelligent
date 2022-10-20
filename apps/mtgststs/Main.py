#!/usr/bin/env python
# -*- encoding:utf8 -*-
# Flask などの必要なライブラリをインポートする
from flask import Flask
import importlib
import json
import os
import logging
from config.loggingConfig import LOGGING
from flaskext.versioned import Versioned
import re
import hashlib

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__, static_url_path='/static')
versioned = Versioned(app, format='/%(path)s?v=%(version)s')

#md5
def md5_image(file_name, lang):
    file_name = str(file_name.encode('utf-8')) + '_' + str(lang)
    return hashlib.md5(file_name.encode('utf-8')).hexdigest()

app.jinja_env.filters['md5_image'] = md5_image

#regrex
def re_sub(text, pattern, replace):
    return re.sub(pattern, replace, text)

app.jinja_env.filters['re_sub'] = re_sub

#設定
s = open(os.path.dirname(__file__) + "/config/config.json" ,"r")
config =json.load(s)
s.close()

#utilities
utils = importlib.import_module("utils.Utilities")

#logging
logging.config.dictConfig(LOGGING)
log = importlib.import_module("utils.logging")

#controllerをimport
import controllers.ControllerManager

if __name__ == "__main__":
    app.run(host='0.0.0.0:8080', debug=True)
