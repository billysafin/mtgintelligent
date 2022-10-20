#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class ArticlesJp(DB.Model):
    __tablename__ = 'mtg_reading'
    __bind_key__ = 'info'
    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    published   = DB.Column(DB.DateTime, nullable=False)
    title       = DB.Column(DB.Text(), nullable=False)
    link        = DB.Column(DB.Text(), nullable=False)
    date        = DB.Column(DB.DateTime, nullable=False)
    source_from = DB.Column(DB.Text(), nullable=False)
    delete_flag = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<ArticlesJp(id='%s', published='%s', title='%s',  link='%s', date='%s', source_from='%s', delete_flag='%s')>" % (
            self.id, self.published, self.title, self.link, self.date, self.source_from, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'published'     : self.published,
            'title'         : self.title,
            'link'          : self.link,
            'date'          : self.date,
            'source_from'   : self.source_from,
            'delete_flag'   : self.delete_flag
        }