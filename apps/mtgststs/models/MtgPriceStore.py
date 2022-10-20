#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgPriceStore(DB.Model):
    __tablename__ = 'mtg_price_store'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name            = DB.Column(DB.Text, nullable=False)
    url             = DB.Column(DB.Text, nullable=False)
    api             = DB.Column(DB.Text, nullable=False)
    is_auction      = DB.Column(DB.Integer, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgPriceStore(id='%s', name='%s', url='%s',  api='%s', is_auction='%s', delete_flag='%s')>" % (
            self.id, self.name, self.url, self.api, self.is_auction, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'url'           : self.url,
            'api'           : self.api,
            'is_auction'    : self.is_auction,
            'delete_flag'   : self.delete_flag
        }