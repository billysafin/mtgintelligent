# -*- encoding:utf8 -*-
from services.ServiceManager import sql_logging
from sqlalchemy import *
from models.MtgDecklistPlayedCardsStats import MtgDecklistPlayedCardsStats

#get players by tour id
@sql_logging
def getPlayersbyTourId(tour_id):
    query = MtgPlayerRecord.query.join(MtgPlayer, MtgPlayer.id == MtgPlayerRecord.player_id)
    query = query.filter(MtgPlayerRecord.tournament_id == tour_id).order_by(MtgPlayerRecord.rank.desc())
    query = query.all()
    
    return query
