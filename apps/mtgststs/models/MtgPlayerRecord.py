#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgPlayerRecord(DB.Model):
    __tablename__ = 'mtg_player_record'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    player_id       = DB.Column(DB.Integer, nullable=False)
    rank            = DB.Column(DB.Integer, nullable=False)
    omwp            = DB.Column(DB.Integer, nullable=False)
    gwp             = DB.Column(DB.Integer, nullable=False)
    ogwp            = DB.Column(DB.Integer, nullable=False)
    tournament_id   = DB.Column(DB.Integer, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgPlayerRecord(id='%s', player_id='%s', tournament_id='%s',  rank='%s', omwp='%s', gwp='%s', ogwp='%s', points='%s', delete_flag='%s')>" % (
            self.id, self.player_id, self.tournament_id, self.rank, self.omwp, self.gwp, self.ogwp, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                    : self.id,
            'player_id'             : self.player_id,
            'tournament_id'         : self.tournament_id,
            'rank'                  : self.rank,
            'omwp'                  : self.omwp,
            'gwp'                   : self.gwp,
            'ogwp'                  : self.ogwp,
            'points'                : self.points,
            'delete_flag'           : self.delete_flag
        }
