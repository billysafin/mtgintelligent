#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgCardSubSetName(DB.Model):
    __tablename__ = 'mtg_card_sub_set_name'
    __bind_key__ = 'info'
    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    mtg_card_main_id    = DB.Column(DB.Integer, nullable=False)
    set_name            = DB.Column(DB.Text(), nullable=False)
    delete_flag         = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgCardSubSetName(id='%s', mtg_card_main_id='%s', set_name='%s', delete_flag='%s')>" % (
            self.id, self.mtg_card_main_id, self.set_name, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'mtg_card_main_id'  : self.mtg_card_main_id,
            'set_name'          : self.set_name,
            'delete_flag'       : self.delete_flag
        }