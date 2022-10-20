#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgCardImage(DB.Model):
    __tablename__ = 'mtg_card_image'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    mtg_card_id     = DB.Column(DB.Integer, nullable=False)
    edition_id      = DB.Column(DB.Integer, nullable=False)
    country_id      = DB.Column(DB.Integer, nullable=False)
    image           = DB.Column(DB.Text(), nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgCardImage(id='%s', mtg_card_id='%s', edition_id='%s',  country_id='%s', image='%s', delete_flag='%s')>" % (
            self.id, self.mtg_card_id, self.edition_id, self.country_id, self.image, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'mtg_card_id'   : self.mtg_card_id,
            'edition_id'    : self.edition_id,
            'image'         : self.image,
            'country_id '   : self.country_id ,
            'delete_flag'   : self.delete_flag
        }