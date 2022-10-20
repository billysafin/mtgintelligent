#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgCardUsageAggregate(DB.Model):
    __tablename__ = 'mtg_card_usage_aggregate'
    __bind_key__ = 'info'
    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    meta_id             = DB.Column(DB.Integer, nullable=False)
    card_id             = DB.Column(DB.Integer, nullable=False)
    amount              = DB.Column(DB.Integer, nullable=False)
    where_board         = DB.Column(DB.Integer, nullable=False)
    player_count        = DB.Column(DB.Integer, nullable=False)
    total_players       = DB.Column(DB.Integer, nullable=False)
    date                = DB.Column(DB.DateTime, nullable=False)
    delete_flag         = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgCardUsageAggregate(id='%s', meta_id='%s', card_id='%s', amount='%s', where_board='%s', player_count='%s', total_players='%s', date='%s', delete_flag='%s')>" % (
            self.id, self.meta_id, self.card_id, self.amount, self.where_board, self.player_count, self.total_players, self.date, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'meta_id'           : self.meta_id,
            'card_id'           : self.card_id,
            'amount'            : self.amount,
            'where_board'       : self.where_board,
            'player_count'      : self.player_count,
            'total_players'     : self.total_players,
            'date'              : self.date,
            'delete_flag'       : self.delete_flag
        }