#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgDeckCountByDateAggregate(DB.Model):
    __tablename__ = 'mtg_deck_count_by_date_aggregate'
    __bind_key__ = 'info'
    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    meta_id             = DB.Column(DB.Integer, nullable=False)
    start               = DB.Column(DB.DateTime, nullable=False)
    end                 = DB.Column(DB.DateTime, nullable=False)
    name                = DB.Column(DB.Text(), nullable=False)
    count               = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgDeckCountByDateAggregate(id='%s', meta_id='%s', start='%s',  end='%s',  name='%s',  count='%s')>" % (
            self.id, self.meta_id, self.start, self.end, self.name, self.count)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'meta_id'       : self.meta_id,
            'start'         : self.start,
            'end'           : self.end,
            'name'          : self.name,
            'count'         : self.count
        }