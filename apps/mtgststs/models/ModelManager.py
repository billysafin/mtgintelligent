# -*- encoding:utf8 -*-
from Main import app, config
from flask_sqlalchemy import SQLAlchemy

#db関連
for key, value in config['db'].items():
    app.config[key] = value
DB = SQLAlchemy(app)

#jsonフォーマット化
def to_json(inst, cls):
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)
