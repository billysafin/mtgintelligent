#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgEvents(DB.Model):
    __tablename__ = 'mtg_events'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    date            = DB.Column(DB.DateTime, nullable=False)
    type            = DB.Column(DB.Text(), nullable=False)
    format          = DB.Column(DB.Text(), nullable=False)
    store           = DB.Column(DB.Text(), nullable=False)
    location        = DB.Column(DB.Text(), nullable=False)
    email           = DB.Column(DB.Text(), nullable=False)
    obtained_date   = DB.Column(DB.DateTime, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgEvents(id='%s', date='%s', type='%s', name='%s', format='%s', store='%s', location='%s', email='%s', obtained_date='%s', delete_flag='%s')>" % (
            self.id, self.date, self.type, self.name, self.format, self.store, self.location, self.email, self.obtained_date, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'date'              : self.date,
            'type'              : self.type,
            'name'              : self.name,
            'format'            : self.format,
            'store'             : self.store,
            'location'          : self.location,
            'email'             : self.email,
            'obtained_date'     : self.obtained_date,
            'delete_flag'       : self.delete_flag
        }