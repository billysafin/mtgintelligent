#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgFormat(DB.Model):
    __tablename__ = 'mtg_format'
    __bind_key__ = 'info'
    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    format_en   = DB.Column(DB.Text(), nullable=False)
    format_jp   = DB.Column(DB.Text(), nullable=False)
    delete_flag = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgFormat(id='%s', format_en='%s', format_jp='%s', delete_flag='%s')>" % (
            self.id, self.format_en, self.format_jp, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'format_en'     : self.format_en,
            'format_jp'     : self.format_jp,
            'delete_flag'   : self.delete_flag
        }