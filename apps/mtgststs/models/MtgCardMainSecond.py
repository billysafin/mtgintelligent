#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgCardMainSecond(DB.Model):
    __tablename__ = 'mtg_card_main_second'
    __bind_key__ = 'info'
    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    mtg_card_main_id    = DB.Column(DB.Integer, nullable=False)
    color               = DB.Column(DB.Text(), nullable=False)
    converted_mana_cost = DB.Column(DB.Text(), nullable=False)
    mana_cost           = DB.Column(DB.Text(), nullable=False)
    type                = DB.Column(DB.Text(), nullable=False)
    power               = DB.Column(DB.Text(), nullable=False)
    thoughness          = DB.Column(DB.Text(), nullable=False)
    loyalty             = DB.Column(DB.Text(), nullable=False)
    text_en             = DB.Column(DB.Text(), nullable=False)
    delete_flag         = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<ClickCount(id='%s', mtg_card_main_id='%s', color='%s',  converted_mana_cost='%s', mana_cost='%s', type='%s', power='%s', thoughness='%s', loyalty='%s', text_en='%s', delete_flag='%s')>" % (
            self.id, self.mtg_card_main_id, self.color, self.converted_mana_cost, self.mana_cost, self.power, self.type, self.thoughness, self.loyalty, self.text_en, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                    : self.id,
            'mtg_card_main_id'      : self.mtg_card_main_id,
            'color'                 : self.color,
            'converted_mana_cost'   : self.converted_mana_cost,
            'mana_cost'             : self.mana_cost,
            'type'                  : self.type,
            'power'                 : self.power,
            'thoughness'            : self.thoughness,
            'loyalty'               : self.loyalty,
            'text_en'               : self.text_en,
            'delete_flag'           : self.delete_flag
        }