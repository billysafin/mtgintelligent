# -*- encoding:utf8 -*-
import datetime
from models.MtgCard import MtgCard
from models.MtgCardMain import MtgCardMain
from models.MtgCardMainJp import MtgCardMainJp
from models.MtgDecklist import MtgDecklist
from models.MtgDecklistDetail import MtgDecklistDetail
from models.MtgMetaName import MtgMetaName
from models.MtgPlayer import MtgPlayer
from models.MtgPlayerRecord import MtgPlayerRecord
from models.MtgFormat import MtgFormat
from models.MtgTournament import MtgTournament
from models.MtgCardUsageAggregate import MtgCardUsageAggregate
from models.MtgDecklistWhere import MtgDecklistWhere
from models.MtgCardImage import MtgCardImage
from services.ServiceManager import sql_logging, geoCheck
from sqlalchemy import *
from datetime import date
from dateutil.relativedelta import relativedelta
import re

TO_DATE = datetime.date.today().strftime('%Y-%m-%d')

#get number of decks by decklist id
@sql_logging
def getDecklistAmountByDecklistId(did, from_date=None, to_date=None):
    query = MtgTournament.query.join(MtgDecklist, MtgDecklist.tournament_id == MtgTournament.id)
    query = query.with_entities(func.date_format(MtgTournament.start, '%Y-%m').label('date'), func.count(MtgDecklist.id).label('count'))
    
    today = date.today()
    six_month_ago = today - relativedelta(months=6)
    if from_date is None or from_date is True:
        query = query.filter(MtgTournament.start >= six_month_ago.strftime('%Y-%m-%d'))
    elif from_date is not None and from_date is not True:
        query = query.filter(MtgTournament.start >= from_date)
        
    if to_date is None  or to_date is True:
        query = query.filter(MtgTournament.start <= today.strftime('%Y-%m-%d'))
    elif to_date is not None and to_date is not True:
        query = query.filter(MtgTournament.start <= to_date)
    
    query = query.filter(MtgDecklist.meta_deck_name_id == did)
    query = query.filter(MtgTournament.delete_flag == 0)
    query = query.group_by(func.date_format(MtgTournament.start, '%Y-%m'))
    query = query.all()
    
    return query

#get decklists by deck id
@sql_logging
def getDecklistByDecklistId(did, offset = None, limit = None, from_date = None, to_date = None):
    geo = geoCheck()
    
    sub = MtgDecklist.query.with_entities(MtgDecklist.id.label('deck_id'))
    sub = sub.join(MtgMetaName, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    sub = sub.filter(MtgDecklist.delete_flag == 0)
    sub = sub.filter(MtgMetaName.id == did)
    sub = sub.join(MtgTournament, MtgTournament.id == MtgDecklist.tournament_id)
    
    today = date.today()
    half_year_ago = today - relativedelta(months=6)
    if from_date is not None:
        sub = sub.filter(MtgTournament.start >= from_date)
        
    if to_date is not None:
        sub = sub.filter(MtgTournament.start <= to_date)
        
    sub = sub.order_by(MtgTournament.start.desc())
        
    if offset is not None:
        sub = sub.offset(offset)
    
    if limit is not None:
        sub = sub.limit(limit)    
    
    sub = sub.all()
    
    if sub is '' or sub is None:
        return None
    
    ids = []
    for id in sub:
        ids.append(str(id[0]))
        
    query = MtgDecklist.query.join(MtgMetaName, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    query = query.join(MtgDecklistDetail, MtgDecklist.id == MtgDecklistDetail.decklist_id)
    query = query.join(MtgCard, MtgCard.id == MtgDecklistDetail.card_id)
    query = query.join(MtgCardMain, MtgCard.id == MtgCardMain.mtg_card_id)
    query = query.join(MtgPlayer, MtgDecklist.player_id == MtgPlayer.id)
    query = query.join(MtgTournament, MtgTournament.id == MtgDecklist.tournament_id)
    
    if geo == 'ja':
        country_id = 2
        query = query.outerjoin(MtgCardMainJp, MtgCardMain.id == MtgCardMainJp.mtg_card_main_id)
    else:
        country_id = 3
        
    subImage = MtgCardImage.query.filter(MtgCardImage.country_id == country_id).order_by(MtgCardImage.edition_id.desc()).subquery("image")
    query = query.join(subImage, subImage.c.mtg_card_id == MtgCard.id)
    
    query = query.with_entities(
        MtgPlayer.name.label('player_name'),
        MtgPlayer.id.label('player_id'),
        MtgDecklistDetail.mtg_decklist_where_id.label('which'),
        MtgDecklistDetail.used_amount.label('total'),
        MtgCardMain.type.label('card_type'),
        MtgCard.url.label('card_url'),
        subImage.c.image.label('image_name'),
        MtgTournament.start.label('date')
    )
    
    if geo == 'ja':
        query = query.add_column(func.IF(MtgCardMainJp.name_jp != null,MtgCardMainJp.name_jp,MtgCard.name).label('card_name'))
        query = query.add_column(MtgCard.name.label('card_name_en'))
    else:
        query = query.add_column(MtgCard.name.label('card_name'))
        query = query.add_column(MtgCard.name.label('card_name_en'))
    
    query = query.filter(MtgMetaName.id == did)
    query = query.filter(MtgMetaName.delete_flag == 0)
    query = query.filter(MtgDecklist.id.in_(ids))
    query = query.order_by(MtgTournament.start.desc())
    
    query = query.all()
    
    return query

#get decklist by meta deck name
@sql_logging
def getDecklistByMetaName(meta_name, format_id):
    geo = geoCheck()
    
    sub = MtgMetaName.query.join(MtgDecklist, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    sub = sub.join(MtgPlayer, MtgDecklist.player_id == MtgPlayer.id)
    sub = sub.with_entities(MtgPlayer.name.label('player_name'))
    sub = sub.filter(MtgMetaName.name == meta_name)
    sub = sub.filter(MtgMetaName.mtg_format_id == format_id)
    sub = sub.filter(MtgMetaName.delete_flag == 0)
    sub = sub.group_by(MtgPlayer.name)
    sub = sub.limit(1)
    
    if sub[0].player_name is '' or sub[0].player_name is None:
        return None
    
    query = MtgMetaName.query.join(MtgDecklist, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    query = query.join(MtgDecklistDetail, MtgDecklist.id == MtgDecklistDetail.decklist_id)
    query = query.join(MtgCard, MtgCard.id == MtgDecklistDetail.card_id)
    query = query.join(MtgCardMain, MtgCard.id == MtgCardMain.mtg_card_id)
    
    if geo == 'ja':
        country_id = 2
        query = query.outerjoin(MtgCardMainJp, MtgCardMain.id == MtgCardMainJp.mtg_card_main_id)
    else:
        country_id = 3
    
    query = query.join(MtgPlayer, MtgDecklist.player_id == MtgPlayer.id)
    
    subImage = MtgCardImage.query.filter(MtgCardImage.country_id == country_id).order_by(MtgCardImage.edition_id.desc()).subquery("image")
    query = query.join(subImage, subImage.c.mtg_card_id == MtgCard.id)
    
    query = query.with_entities(
        MtgPlayer.name.label('player_name'),
        MtgDecklistDetail.mtg_decklist_where_id.label('which'),
        MtgDecklistDetail.used_amount.label('total'),
        MtgCardMain.type.label('card_type'),
        MtgCard.url.label('card_url'),
        subImage.c.image.label('image_name')
    )
    
    if geo == 'ja':
        query = query.add_column(func.IF(MtgCardMainJp.name_jp != null,MtgCardMainJp.name_jp,MtgCard.name).label('card_name'))
        query = query.add_column(MtgCard.name.label('card_name_en'))
    else:
        query = query.add_column(MtgCard.name.label('card_name'))
        query = query.add_column(MtgCard.name.label('card_name_en'))
    
    query = query.filter(MtgMetaName.name == meta_name)
    query = query.filter(MtgMetaName.mtg_format_id == format_id)
    query = query.filter(MtgMetaName.delete_flag == 0)
    query = query.filter(MtgPlayer.name == sub[0].player_name)
    query = query.all()
    
    return query

#get decklist by player id
@sql_logging
def getDecklistByTourId(tour_id):
    geo = geoCheck()
    
    query = MtgDecklist.query.outerjoin(MtgMetaName, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    query = query.join(MtgDecklistDetail, MtgDecklist.id == MtgDecklistDetail.decklist_id)
    query = query.join(MtgCard, MtgCard.id == MtgDecklistDetail.card_id)
    query = query.join(MtgCardMain, MtgCard.id == MtgCardMain.mtg_card_id)
    query = query.join(MtgPlayer, MtgDecklist.player_id == MtgPlayer.id)
    
    sub = MtgPlayerRecord.query.filter(MtgPlayerRecord.tournament_id == tour_id)
    sub = sub.filter(MtgPlayerRecord.delete_flag == 0).subquery()
    
    query = query.join(sub, sub.c.player_id == MtgPlayer.id)
    
    if geo == 'ja':
        country_id = 2
        query = query.join(MtgCardMainJp, MtgCardMain.id == MtgCardMainJp.mtg_card_main_id)
    else:
        country_id = 3
    
    subImage = MtgCardImage.query.filter(MtgCardImage.country_id == country_id).order_by(MtgCardImage.edition_id.desc()).subquery("image")
    query = query.join(subImage, subImage.c.mtg_card_id == MtgCard.id)
    
    query = query.with_entities(
        MtgCardMain.type.label('card_type'),
        MtgCard.url.label('card_url'),
        sub.c.rank.label('player_rank'),
        sub.c.omwp.label('player_omwp'),
        sub.c.gwp.label('player_gwp'),
        sub.c.ogwp.label('player_ogwp'),
        MtgPlayer.name.label('player_name'),
        MtgMetaName.name.label('meta_name'),
        MtgDecklistDetail.mtg_decklist_where_id.label('which'),
        MtgDecklistDetail.used_amount.label('total'),
        subImage.c.image.label('image_name')
    )
    
    if geo == 'ja':
        query = query.add_column(func.IF(MtgCardMainJp.name_jp != '',MtgCardMainJp.name_jp,MtgCard.name).label('card_name'))
        query = query.add_column(MtgCard.name.label('card_name_en'))
    else:
        query = query.add_column(MtgCard.name.label('card_name'))
        query = query.add_column(MtgCard.name.label('card_name_en'))
    
    query = query.filter(MtgDecklist.tournament_id == tour_id)
    query = query.filter(MtgPlayer.delete_flag == 0)
    query = query.filter(MtgDecklist.delete_flag == 0)
    query = query.order_by(sub.c.rank).all()
    
    return query

#popular decks
@sql_logging
def getPopularDecks(limit_num, from_date=None, to_date=None):
    geo = geoCheck()
    
    query = MtgDecklist.query.outerjoin(MtgMetaName, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    query = query.outerjoin(MtgTournament, MtgTournament.id == MtgDecklist.tournament_id)
    query = query.outerjoin(MtgFormat, MtgFormat.id == MtgMetaName.mtg_format_id)
    query = query.filter(MtgMetaName.name != '')
    query = query.group_by(MtgMetaName.mtg_format_id, MtgMetaName.name)
    query = query.order_by(func.count(MtgDecklist.id).desc())
    query = query.with_entities(MtgMetaName.id.label('id'), MtgMetaName.name.label('name'), func.count(MtgDecklist.id).label('count'), MtgFormat.format_en.label('format_name'))
    
    today = date.today()
    half_year_ago = today - relativedelta(months=6)
    if from_date is not None:
        query = query.filter(MtgTournament.start >= half_year_ago.strftime('%Y-%m-%d'))
        
    if to_date is not None:
        query = query.filter(MtgTournament.start <= today.strftime('%Y-%m-%d'))
    
    if limit_num is None:
        limit_num = 10
    
    query = query.limit(limit_num).all()
    
    return query

#popular decks
@sql_logging
def getDeckNameByDid(did):
    query = MtgDecklist.query.outerjoin(MtgMetaName, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    query = query.with_entities(MtgMetaName.name.label('name'))
    query = query.filter(MtgMetaName.id == did)
    query = query.filter(MtgMetaName.delete_flag == 0)
    
    query = query.limit(1).all()
    
    return query

#popular decks
@sql_logging
def getDeckIdByName(name):
    query = MtgDecklist.query.outerjoin(MtgMetaName, MtgMetaName.id == MtgDecklist.meta_deck_name_id)
    query = query.with_entities(MtgDecklist.id.label('did'))
    query = query.filter(MtgMetaName.name == meta_deck_name_id)
    query = query.filter(MtgMetaName.delete_flag == 0)
    
    query = query.limit(1).all()
    
    return query[0]

#popular decks
@sql_logging
def getMtgCardUsageByMetaId(meta_id, limit_by=None, where_board=None, from_date=None, to_date=None):
    geo = geoCheck()
    
    query = MtgCardUsageAggregate.query.join(MtgCard, MtgCard.id == MtgCardUsageAggregate.card_id)
    query = query.join(MtgCardMain, MtgCardMain.mtg_card_id == MtgCard.id)
    query = query.join(MtgDecklistWhere, MtgDecklistWhere.id == MtgCardUsageAggregate.where_board)
    
    if geo == 'ja':
        country_id = 2
        query = query.join(MtgCardMainJp, MtgCardMainJp.mtg_card_main_id == MtgCardMain.id)
        query = query.filter(MtgCardMainJp.delete_flag == 0)
    else:
        country_id = 3
        
    query = query.filter(MtgCardUsageAggregate.meta_id == meta_id)
    query = query.filter(MtgCardUsageAggregate.delete_flag == 0)
    query = query.filter(MtgCard.delete_flag == 0)
    query = query.filter(MtgCardMain.delete_flag == 0)
    
    if where_board is not None:
        query = query.filter(MtgDecklistWhere.id == where_board)
        
    subImage = MtgCardImage.query.filter(MtgCardImage.country_id == country_id).order_by(MtgCardImage.edition_id.desc()).subquery("image")
    query = query.join(subImage, subImage.c.mtg_card_id == MtgCard.id)
    
    query = query.with_entities(
        MtgCard.url,
        MtgDecklistWhere.where_board,
        MtgCardUsageAggregate.amount,
        MtgCardUsageAggregate.player_count,
        MtgCardUsageAggregate.total_players,
        subImage.c.image.label('image_name')
    )
    
    if geo == 'ja':
        query = query.add_column(MtgCardMainJp.name_jp.label('card_name'))
        query = query.add_column(MtgCard.name.label('card_name_en'))
    else:
        query = query.add_column(MtgCard.name.label('card_name'))
        query = query.add_column(MtgCard.name.label('card_name_en'))
    
    if from_date is not None:
        from_date = re.sub(r'-01$', r'-01', from_date)
        query = query.filter(MtgCardUsageAggregate.date >= from_date)
        
    if to_date is not None:
        to_date = re.sub(r'-[0-2][0-9]$', r'-01', to_date)
        query = query.filter(MtgCardUsageAggregate.date <= to_date)
    
    query = query.group_by(MtgCard.url, MtgCardUsageAggregate.amount)
    
    if limit_by is None:
        query = query.order_by("date desc", "player_count desc").all()
    else:
        query = query.order_by("date desc", "player_count desc").limit(limit_by).all()
        
    return query