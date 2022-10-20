#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgMetaName(DB.Model):
    __tablename__ = 'mtg_meta_name'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name            = DB.Column(DB.Text(), nullable=False)
    mtg_format_id   = DB.Column(DB.Integer, nullable=False)
    rotation_date   = DB.Column(DB.DateTime, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgMetaName(id='%s', name='%s', mtg_format_id='%s',  rotation_date='%s', delete_flag='%s')>" % (
            self.id, self.name, self.mtg_format_id, self.rotation_date, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'name'              : self.name,
            'mtg_format_id'     : self.mtg_format_id,
            'rotation_date'     : self.rotation_date,
            'delete_flag'       : self.delete_flag
        }