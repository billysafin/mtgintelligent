#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgDraftPicks(DB.Model):
    __tablename__ = 'mtg_draft_picks'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    player_id       = DB.Column(DB.Integer, nullable=False)
    draft_pod_id    = DB.Column(DB.Integer, nullable=False)
    pack_number     = DB.Column(DB.Integer, nullable=False)
    picked_number   = DB.Column(DB.Integer, nullable=False)
    picked_card_id  = DB.Column(DB.Integer, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgDraftPicks(id='%s', player_id='%s', pack_number='%s', picked_number='%s', picked_card_id='%s', delete_flag='%s')>" % (
            self.id, self.player_id, self.pack_number, self.picked_number, self.picked_card_id, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'player_id'         : self.player_id,
            'pack_number'       : self.pack_number,
            'picked_number'     : self.picked_number,
            'picked_card_id'    : self.picked_card_id,
            'delete_flag'       : self.delete_flag
        }