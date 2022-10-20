#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class Sites(DB.Model):
    __tablename__ = 'site_names'
    __bind_key__ = 'info'
    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    country_id  = DB.Column(DB.Integer, nullable=False)
    top_link    = DB.Column(DB.Text(), nullable=False)
    site_name   = DB.Column(DB.Text(), nullable=False)
    date        = DB.Column(DB.DateTime, nullable=False)
    image       = DB.Column(DB.Text(), nullable=True)
    delete_flag = DB.Column(DB.Integer, nullable=False)
    
    def __repr__(self):
        return "<Sites(id='%s', country_id='%s', top_link='%s',  site_name='%s', date='%s', image='%s', delete_flag='%s')>" % (
            self.id, self.country_id, self.top_link, self.site_name, self.date, self.image, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'country_id'        : self.country_id,
            'top_link'          : self.top_link,
            'site_name'         : self.site_name,
            'date'              : self.date,
            'image'             : self.image,
            'delete_flag'       : self.delete_flag
        }