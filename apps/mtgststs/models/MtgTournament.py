#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgTournament(DB.Model):
    __tablename__ = 'mtg_tournament'
    __bind_key__ = 'info'
    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    start       = DB.Column(DB.DateTime, nullable=False)
    end         = DB.Column(DB.DateTime, nullable=False)
    country_id  = DB.Column(DB.Integer, nullable=False)
    name        = DB.Column(DB.Text(), nullable=False)
    rounds      = DB.Column(DB.Integer, nullable=False)
    format      = DB.Column(DB.Integer, nullable=False)
    memo        = DB.Column(DB.Text(), nullable=False)
    delete_flag = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgTournament(id='%s', start='%s', end='%s',  country_id='%s', name='%s', rounds='%s', format='%s', memo='%s', delete_flag='%s')>" % (
            self.id, self.start, self.end, self.country_id, self.name, self.rounds, self.format, self.memo, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                    : self.id,
            'start'                 : self.start,
            'end'                   : self.end,
            'country_id'            : self.country_id,
            'name'                  : self.name,
            'rounds'                : self.rounds,
            'format'                : self.format,
            'memo'                  : self.memo,
            'delete_flag'           : self.delete_flag
        }