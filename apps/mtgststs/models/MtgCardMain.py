#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgCardMain(DB.Model):
    __tablename__ = 'mtg_card_main'
    __bind_key__ = 'info'
    id                   = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    mtg_card_id          = DB.Column(DB.Integer, nullable=False)
    color                = DB.Column(DB.Text(), nullable=False)
    mana_cost            = DB.Column(DB.Text(), nullable=False)
    type                 = DB.Column(DB.Text(), nullable=False)
    power                = DB.Column(DB.Text(), nullable=False)
    thoughness           = DB.Column(DB.Text(), nullable=False)
    loyalty              = DB.Column(DB.Text(), nullable=False)
    text_en              = DB.Column(DB.Text(), nullable=False)
    second_card_form     = DB.Column(DB.Text(), nullable=False)
    delete_flag          = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgCardMain(id='%s', mtg_card_id='%s', color='%s',  mana_cost='%s', type='%s', power='%s', thoughness='%s', loyalty='%s', text_en='%s', second_card_form='%s',  delete_flag='%s')>" % (
            self.mtg_card_id, self.color, self.mana_cost, self.type, self.power, self.thoughness, self.loyalty, self.text_en, self.second_card_form, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'mtg_card_id'       : self.mtg_card_id,
            'color'             : self.color,
            'mana_cost'         : self.mana_cost,
            'type'              : self.type,
            'power'             : self.power,
            'thoughness'        : self.thoughness,
            'loyalty'           : self.loyalty,
            'text_en'           : self.text_en,
            'second_card_form'  : self.second_card_form,
            'delete_flag'       : self.delete_flag,
        }