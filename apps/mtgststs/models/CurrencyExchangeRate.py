#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class CurrencyExchangeRate(DB.Model):
    __tablename__ = 'currency_exchange_rate'
    __bind_key__ = 'info'
    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    currency_id_from    = DB.Column(DB.Integer, nullable=False)
    currency_id_to      = DB.Column(DB.Integer, nullable=False)
    exchange_rate       = DB.Column(DB.Float, nullable=False)
    delete_flag         = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<CurrencyExchangeRate(id='%s', currency_id_from='%s', currency_id_to='%s', exchange_rate='%s', delete_flag='%s')>" % (
            self.id, self.currency_id_from, self.currency_id_to, self.exchange_rate, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'currency_id_from'  : self.currency_id_from,
            'currency_id_to'    : self.currency_id_to,
            'exchange_rate'     : self.exchange_rate,
            'delete_flag'       : self.delete_flag
        }