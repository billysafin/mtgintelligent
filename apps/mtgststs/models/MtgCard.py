#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgCard(DB.Model):
    __tablename__ = 'mtg_card'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name            = DB.Column(DB.Text(), nullable=False)
    url             = DB.Column(DB.Text(), nullable=False)
    obtained_flag   = DB.Column(DB.Integer, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgCard(id='%s', name='%s', url='%s',  obtained_flag='%s', delete_flag='%s')>" % (
            self.id, self.name, self.url, self.obtained_flag, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'url'           : self.url,
            'obtained_flag' : self.obtained_flag,
            'delete_flag'   : self.delete_flag
        }