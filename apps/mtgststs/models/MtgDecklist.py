#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgDecklist(DB.Model):
    __tablename__ = 'mtg_decklist'
    __bind_key__ = 'info'
    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    player_id           = DB.Column(DB.Integer, nullable=False)
    tournament_id       = DB.Column(DB.Integer, nullable=False)
    meta_deck_name_id   = DB.Column(DB.Integer, nullable=False)
    memo                = DB.Column(DB.Text(), nullable=False)
    delete_flag         = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgDecklist(id='%s', player_id='%s', tournament_id='%s',  meta_deck_name_id='%s', memo='%s', delete_flag='%s')>" % (
            self.id, self.player_id, self.tournament_id, self.meta_deck_name_id, self.memo, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                        : self.id,
            'player_id'                 : self.player_id,
            'tournament_id'             : self.tournament_id,
            'meta_deck_name_id'         : self.meta_deck_name_id,
            'memo'                      : self.memo,
            'delete_flag'               : self.delete_flag
        }