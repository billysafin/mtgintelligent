#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgDraftPickWeight(DB.Model):
    __tablename__ = 'mtg_draft_pick_weight'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    mtg_card_id     = DB.Column(DB.Integer, nullable=False)
    edition_id      = DB.Column(DB.Integer, nullable=False)
    pick_weight     = DB.Column(DB.Float, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgDraftPickWeight(id='%s', mtg_card_id='%s', edition_id='%s',  pick_weight='%s', delete_flag='%s')>" % (
            self.id, self.mtg_card_id, self.edition_id, self.pick_weight, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'mtg_card_id'   : self.draft_pod_id,
            'edition_id'    : self.pack_number,
            'pick_weight'   : self.edition_id,
            'delete_flag'   : self.delete_flag
        }