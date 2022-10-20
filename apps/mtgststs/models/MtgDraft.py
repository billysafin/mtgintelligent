#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgDraft(DB.Model):
    __tablename__ = 'mtg_draft'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    draft_pod_id    = DB.Column(DB.Integer, nullable=False)
    pack_number     = DB.Column(DB.Integer, nullable=False)
    edition_id      = DB.Column(DB.Integer, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgDraft(id='%s', draft_pod_id='%s', pack_number='%s',  edition_id='%s', delete_flag='%s')>" % (
            self.id, self.draft_pod_id, self.pack_number, self.edition_id, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'draft_pod_id'  : self.draft_pod_id,
            'pack_number'   : self.pack_number,
            'edition_id'    : self.edition_id,
            'delete_flag'   : self.delete_flag
        }