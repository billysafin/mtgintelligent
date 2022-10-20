#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgDecklistPlayedCardsStats(DB.Model):
    __tablename__ = 'mtg_decklist_played_cards_stats'
    __bind_key__ = 'info'
    
    id                      = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    mtg_decklist_id         = DB.Column(DB.Integer, nullable=False)
    mtg_card_id             = DB.Column(DB.Integer, nullable=False)
    where_board             = DB.Column(DB.Integer, nullable=False)
    amount                  = DB.Column(DB.Integer, nullable=False)
    total_players           = DB.Column(DB.Integer, nullable=False)
    delete_flag             = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "<MtgDecklistPlayedCardsStats(id='%s', mtg_decklist_id='%s', mtg_card_id='%s',  where_board='%s', amount='%s', total_players='%s', delete_flag='%s')>" % (
            self.id, self.mtg_decklist_id, self.mtg_card_id, self.where_board, self.amount, self.total_players, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                    : self.id,
            'mtg_decklist_id'       : self.mtg_decklist_id,
            'mtg_card_id'           : self.mtg_card_id,
            'where_board'           : self.where_board,
            'amount'                : self.amount,
            'total_players'         : self.total_players,
            'delete_flag'           : self.delete_flag
        }