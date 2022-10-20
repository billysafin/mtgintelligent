#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgDecklistDetail(DB.Model):
    __tablename__ = 'mtg_decklist_detail'
    __bind_key__ = 'info'
    id                      = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    decklist_id             = DB.Column(DB.Integer, nullable=False)
    mtg_decklist_where_id   = DB.Column(DB.Integer, nullable=False)
    used_amount             = DB.Column(DB.Integer, nullable=False)
    card_id                 = DB.Column(DB.Integer, nullable=False)
    memo                    = DB.Column(DB.Text(), nullable=False)
    delete_flag             = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgDecklistDetail(id='%s', decklist_id='%s', mtg_decklist_where_id='%s',  used_amount='%s', card_id='%s', memo='%s', delete_flag='%s')>" % (
            self.id, self.href, self.mtg_decklist_where_id, self.used_amount, self.card_id, self.memo, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                            : self.id,
            'decklist_id'                   : self.decklist_id,
            'mtg_decklist_where_id'         : self.mtg_decklist_where_id,
            'used_amount'                   : self.used_amount,
            'card_id'                       : self.card_id,
            'memo'                          : self.memo,
            'delete_flag'                   : self.delete_flag
        }