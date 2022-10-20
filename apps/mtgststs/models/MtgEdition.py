#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgEdition(DB.Model):
    __tablename__ = 'mtg_edition'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    short           = DB.Column(DB.Text(), nullable=False)
    name            = DB.Column(DB.Text(), nullable=False)
    name_jp         = DB.Column(DB.Text(), nullable=False)
    is_booster      = DB.Column(DB.Integer, nullable=False)
    booster_sort    = DB.Column(DB.Integer, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgEdition(id='%s', short='%s', name='%s',  name_jp='%s', is_booster='%s', booster_sort='%s', delete_flag='%s')>" % (
            self.id, self.short, self.name, self.name_jp, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'short'         : self.short,
            'name'          : self.name,
            'name_jp'       : self.name_jp,
            'is_booster'    : self.is_booster,
            'booster_sort'  : self.booster_sort,
            'delete_flag'   : self.delete_flag
        }