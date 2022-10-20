#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgPlayer(DB.Model):
    __tablename__ = 'mtg_player'
    __bind_key__ = 'info'
    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name        = DB.Column(DB.Text(), nullable=False)
    memo        = DB.Column(DB.Text(), nullable=False)
    delete_flag = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgPlayer(id='%s', name='%s', memo='%s', delete_flag='%s')>" % (
            self.id, self.name, self.memo, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'href'          : self.name,
            'memo'          : self.memo,
            'delete_flag'   : self.delete_flag
        }