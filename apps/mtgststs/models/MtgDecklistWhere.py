#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgDecklistWhere(DB.Model):
    __tablename__ = 'mtg_decklist_where'
    __bind_key__ = 'info'
    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    where_board = DB.Column(DB.Text(), nullable=False)
    delete_flag = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgDecklistWhere(id='%s', where_board='%s', delete_flag='%s')>" % (
            self.id, self.where_board, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'where_board'   : self.where_board,
            'delete_flag'   : self.delete_flag
        }