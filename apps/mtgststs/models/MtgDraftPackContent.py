#!/usr/bin/env python
# -*- encoding:utf8 -*-
from models.ModelManager import DB

class MtgDraftPackContent(DB.Model):
    __tablename__ = 'mtg_draft_pack_content'
    __bind_key__ = 'info'
    id              = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    player_id       = DB.Column(DB.Integer, nullable=False)
    draft_pod_id    = DB.Column(DB.Integer, nullable=False)
    pack_number     = DB.Column(DB.Integer, nullable=False)
    card_one        = DB.Column(DB.Integer, nullable=False)
    card_two        = DB.Column(DB.Integer, nullable=False)
    card_three      = DB.Column(DB.Integer, nullable=False)
    card_four       = DB.Column(DB.Integer, nullable=False)
    card_five       = DB.Column(DB.Integer, nullable=False)
    card_six        = DB.Column(DB.Integer, nullable=False)
    card_seven      = DB.Column(DB.Integer, nullable=False)
    card_eight      = DB.Column(DB.Integer, nullable=False)
    card_nine       = DB.Column(DB.Integer, nullable=False)
    card_ten        = DB.Column(DB.Integer, nullable=False)
    card_eleven     = DB.Column(DB.Integer, nullable=False)
    card_twelve     = DB.Column(DB.Integer, nullable=False)
    card_thirteen   = DB.Column(DB.Integer, nullable=False)
    card_fourteen   = DB.Column(DB.Integer, nullable=False)
    card_fifteen    = DB.Column(DB.Integer, nullable=False)
    delete_flag     = DB.Column(DB.Integer, nullable=False)
    def __repr__(self):
        return "<MtgDraftPackContent(id='%s', player_id='%s', draft_pod_id='%s',  pack_number='%s', self.card_one, self.card_two, self.card_three, self.card_four, self.card_five, self.card_six, self.card_seven, self.card_eight, self.card_nine, self.card_ten, self.card_eleven, self.card_twelve, self.card_thirteen, self.card_fourteen, self.card_fifteen, delete_flag='%s')>" % (
            self.id, self.player_id, self.draft_pod_id, self.pack_number, self.card_one, self.card_two, self.card_three, self.card_four, self.card_five, self.card_six, self.card_seven, self.card_eight, self.card_nine, self.card_ten, self.card_eleven, self.card_twelve, self.card_thirteen, self.card_fourteen, self.card_fifteen, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'                : self.id,
            'player_id'         : self.player_id,
            'draft_pod_id'      : self.draft_pod_id,  
            'pack_number'       : self.pack_number,   
            'card_one'          : self.card_one,  
            'card_two'          : self.card_two,   
            'card_three'        : self.card_three,   
            'card_four'         : self.card_four, 
            'card_five'         : self.card_five, 
            'card_six'          : self.card_six, 
            'card_seven'        : self.card_seven, 
            'card_eight'        : self.card_eight, 
            'card_nine'         : self.card_nine, 
            'card_ten'          : self.card_ten, 
            'card_eleven'       : self.card_eleven, 
            'card_twelve'       : self.card_twelve, 
            'card_thirteen'     : self.card_thirteen, 
            'card_fourteen'     : self.card_fourteen, 
            'card_fifteen'      : self.card_fifteen, 
            'delete_flag'       : self.delete_flag
        }