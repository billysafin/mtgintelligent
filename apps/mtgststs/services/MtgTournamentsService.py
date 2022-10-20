# -*- encoding:utf8 -*-
from models.MtgTournament import MtgTournament
from models.MtgMetaName import MtgMetaName
from models.MtgDecklist import MtgDecklist
from services.ServiceManager import sql_logging, geoCheck
from sqlalchemy import func
from models.Country import Country
from models.MtgFormat import MtgFormat
from models.MtgDeckCountByDateAggregate import MtgDeckCountByDateAggregate as MtgDeckCountByDateView

#get tournaments
@sql_logging
def Search(format_type, country_id, limit_num, keywords, from_date, to_date, offset):
    query = MtgTournament.query.join(MtgFormat, MtgFormat.id == MtgTournament.format)
    query = query.with_entities(MtgTournament.id, MtgTournament.start, MtgTournament.name, MtgFormat.format_en.label('format_name'))
    
    if country_id is not None:
        query = query.filter(MtgTournament.country_id == country_id)
    #else:
        #query = query.filter(MtgTournament.country_id != 1)
    
    if keywords is not None:
        for word in keywords:
            query = query.filter(MtgTournament.name.like('%' + str(word) + '%'))
    
    if from_date is not None:
        query = query.filter(MtgTournament.start >= from_date)
        
    if to_date is not None:
        query = query.filter(MtgTournament.end <= to_date)
    
    if format_type is not None:
        query = query.filter(MtgTournament.format == format_type)
    
    query = query.filter(MtgTournament.delete_flag != 1)
    query = query.order_by(MtgTournament.start.desc())
    
    if offset is not None:
        query = query.offset(offset)
    
    if limit_num is not None:
        query = query.limit(limit_num)
    else:
        query = query.all()
    return query

#get tournaments
@sql_logging
def getAllTournaments(format_type, country_id, limit_num, offset):
    query = MtgTournament.query.join(MtgFormat, MtgFormat.id == MtgTournament.format)
    query = query.with_entities(MtgTournament.id, MtgTournament.start, MtgTournament.name, MtgFormat.format_en.label('format_name'))
    
    if country_id is not None:
        query = query.filter(MtgTournament.country_id == country_id)
    else:
        query = query.filter(MtgTournament.country_id != 1)
    
    query = query.filter(MtgTournament.delete_flag != 1)
    
    if format_type is not None:
        query = query.filter(MtgTournament.format == format_type)
    
    query = query.order_by(MtgTournament.start.desc())
    
    if offset is not None:
        query = query.offset(offset)
    
    if limit_num is not None:
        query = query.limit(limit_num)
    else:
        query = query.all()
        
    return query

#get tournaments
@sql_logging
def getTournaments(from_date, to_date, format_type, country_id, limit_num):
    kwargs = {}
    kwargs['delete_flag']   = 0
    kwargs['format']        = format_type
    
    if country_id is not None:
        kwargs['country_id']    = country_id
    
    query = MtgTournament.query.with_entities(MtgTournament.id, MtgTournament.start, MtgTournament.end, MtgTournament.name)
    query = query.filter_by(**kwargs).filter(MtgTournament.start >= from_date).filter(MtgTournament.end <= to_date)
    query = query.filter(MtgTournament.country_id != 1)
    
    if limit_num is not None:
        query = query.order_by(MtgTournament.start.desc()).limit(limit_num)
    else:
        query = query.order_by(MtgTournament.start.desc()).all()
        
    return query
    
#get deck type
@sql_logging
def getDeckTypeByFormat(tournament_ids, limit_num, deck_meta_names):
    query = MtgDecklist.query.join(MtgMetaName, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    query = query.with_entities(func.count(MtgMetaName.name).label('count'), MtgMetaName.id.label('deck_id'), MtgMetaName.id.label('did'), MtgMetaName.name.label('name'))
    query = query.filter_by(delete_flag=0)
    query = query.filter(MtgDecklist.tournament_id.in_(tournament_ids))
    
    if deck_meta_names is not None:
        query = query.filter(MtgMetaName.name.in_(deck_meta_names))
    
    query = query.group_by(MtgMetaName.name)
    query = query.order_by('count desc')
    
    if limit_num is not None:
        query = query.limit(limit_num)
    else:
        query = query.all()
    
    return query
 
#get tournaments
@sql_logging
def getDeckTypeCountByFormat(tournament_ids):
    query = MtgDecklist.query.join(MtgMetaName, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    query = query.with_entities(func.count(MtgMetaName.name).label('count'), MtgMetaName.name.label('name'))
    query = query.filter_by(delete_flag=0)
    query = query.filter(MtgDecklist.tournament_id.in_(tournament_ids))
    query = query.group_by(MtgMetaName.name)
    query = query.order_by('count desc')
    query = query.all()
    
    return query
    
#get deck type
@sql_logging
def getTopFiveDeckTypesByFormat(tournament_ids):
    query = MtgDecklist.query.join(MtgMetaName, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    query = query.with_entities(func.count(MtgMetaName.name).label('count'), MtgDecklist.meta_deck_name_id.label('deck_id'), MtgMetaName.name.label('name'))
    query = query.filter_by(delete_flag=0)
    query = query.filter(MtgDecklist.tournament_id.in_(tournament_ids))
    query = query.group_by(MtgMetaName.name)
    query = query.order_by('count desc')
    query = query.limit(5)
    
    return query

#get deck usage total by date and meta name
@sql_logging
def getDeckUsageBYDateMetaNameId(meta_id, from_date, to_date):
    query = MtgDeckCountByDateView.query.join(MtgMetaName, MtgMetaName.id == MtgDeckCountByDateView.meta_id)
    query = query.with_entities(MtgDeckCountByDateView.start.label('start'), MtgDeckCountByDateView.count, MtgDeckCountByDateView.meta_id.label('deck_id'), MtgMetaName.name)
    
    if meta_id is not None:
        query = query.filter(MtgDeckCountByDateView.meta_id == meta_id)
    
    if from_date is not None:
        query = query.filter(MtgDeckCountByDateView.start >= from_date)
    
    if to_date is not None:
        query = query.filter(MtgDeckCountByDateView.end <= to_date)
    
    query = query.order_by('start')
    query = query.all()
    
    return query

#get deck usage total by date and meta name
@sql_logging
def getDeckUsageBYDateMetaNameIdInClause(meta_ids, from_date, to_date):
    query = MtgDeckCountByDateView.query.join(MtgMetaName, MtgMetaName.id == MtgDeckCountByDateView.meta_id)
    query = query.with_entities(MtgDeckCountByDateView.start.label('start'), MtgDeckCountByDateView.count, MtgDeckCountByDateView.meta_id.label('deck_id'), MtgMetaName.name)
    
    if meta_ids is not None:
        query = query.filter(MtgDeckCountByDateView.meta_id.in_(meta_ids))
    
    if from_date is not None:
        query = query.filter(MtgDeckCountByDateView.start >= from_date)
    
    if to_date is not None:
        query = query.filter(MtgDeckCountByDateView.end <= to_date)
    
    query = query.order_by('start')
    query = query.all()
    
    return query

#get deck usage total by date and meta name
@sql_logging
def getDeckUsageBYDateMetaName(deck_meta_name, from_date, to_date, in_clause):
    query = MtgDeckCountByDateView.query.join(MtgMetaName, MtgMetaName.id == MtgDeckCountByDateView.meta_id)
    query = query.with_entities(MtgDeckCountByDateView.start.label('start'), MtgDeckCountByDateView.meta_id, MtgMetaName.name, MtgDeckCountByDateView.count)
    
    if deck_meta_name is not None:
        if in_clause is not None:
            query = query.filter(MtgMetaName.name.in_(deck_meta_name))
        else:
            query = query.filter(MtgMetaName.name == deck_meta_name)
    
    if from_date is not None:
        query = query.filter(MtgDeckCountByDateView.start >= from_date)
    
    if to_date is not None:
        query = query.filter(MtgDeckCountByDateView.end <= to_date)
        
    query = query.order_by('start')
    query = query.all()
    
    return query

#get tournament by id
@sql_logging
def getTournamentById(tour_id):
    geo = geoCheck()
    
    query = MtgTournament.query.join(Country, Country.id == MtgTournament.country_id)
    query = query.join(MtgFormat, MtgFormat.id == MtgTournament.format)
    
    query.with_entities(
        MtgTournament.start,
        MtgTournament.end,
        MtgTournament.name,
        MtgTournament.rounds
    )
    
    if geo == 'ja':
        query = query.add_column(Country.name_jp.label('location'))
        query = query.add_column(MtgFormat.format_jp.label('format_name'))
    else:
        query = query.add_column(Country.name_en.label('location'))
        query = query.add_column(MtgFormat.format_en.label('format_name'))
        
    query = query.filter(MtgTournament.delete_flag == 0)
    query = query.filter(MtgTournament.id == tour_id)
    query = query.limit(1)
    
    return query

#get latest 5
@sql_logging
def getLatestTours(limit_num):
    if limit_num is None:
        limit_num = 5
        
    query = MtgTournament.query.join(MtgFormat, MtgFormat.id == MtgTournament.format)
    query = query.filter(MtgTournament.delete_flag == 0)
    query = query.filter(MtgTournament.country_id != 1)
    query = query.order_by(MtgTournament.start.desc())
    query = query.limit(limit_num)
    query = query.with_entities(MtgTournament.id, MtgTournament.name, MtgTournament.start, MtgFormat.format_en.label('format_name'))
    return query


#get players based on tournament id
@sql_logging
def getPlayersByTour(limit_num, tour_id):
    print("hgeogho")