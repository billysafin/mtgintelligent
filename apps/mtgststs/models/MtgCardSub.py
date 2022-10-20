#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgCardSub(DB.Model):
    __tablename__ = 'mtg_card_sub'
    __bind_key__ = 'info'
    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    mtg_card_main_id    = DB.Column(DB.Integer, nullable=False)
    flavor_text         = DB.Column(DB.Text(), nullable=False)
    artist              = DB.Column(DB.Text(), nullable=False)
    rarity              = DB.Column(DB.Text(), nullable=False)
    set_number          = DB.Column(DB.Text(), nullable=False)
    delete_flag         = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgCardSub(id='%s', mtg_card_main_id='%s', flavor_text='%s', artist='%s', rarity='%s', set_number='%s', delete_flag='%s')>" % (
            self.id, self.mtg_card_main_id, self.flavor_text, self.artist, self.rarity, self.set_number, self.delete_flag)

    @property
    def serialize(self):
        return {
        'id' : self.id,
        'mtg_card_main_id'  : self.mtg_card_main_id,
        'flavor_text'       : self.flavor_text,
        'artist'            : self.artist,
        'rarity'            : self.rarity,
        'set_number'        : self.set_number,
        'delete_flag'       : self.delete_flag
        }