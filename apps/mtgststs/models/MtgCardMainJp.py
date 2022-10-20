#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgCardMainJp(DB.Model):
    __tablename__ = 'mtg_card_main_jp'
    __bind_key__ = 'info'
    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    mtg_card_main_id    = DB.Column(DB.Integer, nullable=False)
    name_jp             = DB.Column(DB.Text(), nullable=False)
    text_jp             = DB.Column(DB.Text(), nullable=False)
    flavor_text_jp      = DB.Column(DB.Text(), nullable=False)
    delete_flag         = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgCardMainJp(id='%s', mtg_card_main_id='%s', name_jp='%s', text_jp='%s', flavor_text_jp='%s', delete_flag='%s')>" % (
            self.id, self.mtg_card_main_id, self.name_jp, self.text_jp, self.flavor_text_jp, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'mtg_card_main_id'  : self.mtg_card_main_id,
            'name_jp'           : self.name_jp,
            'text_jp'           : self.text_jp,
            'flavor_text_jp'    : self.flavor_text_jp,
            'delete_flag'       : self.delete_flag
        }