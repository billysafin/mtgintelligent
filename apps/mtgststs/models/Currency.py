#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class Currency(DB.Model):
    __tablename__ = 'currency'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name            = DB.Column(DB.Text, nullable=False)
    currency_short  = DB.Column(DB.Text, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<Currency(id='%s', name='%s',  currency_short='%s', delete_flag='%s')>" % (
            self.id, self.name, self.currency_short, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'name'              : self.name,
            'currency_short'    : self.currency_short,
            'delete_flag'       : self.delete_flag
        }