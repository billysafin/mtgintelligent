# -*- encoding:utf8 -*-
from services.ServiceManager import sql_logging
from sqlalchemy import *
from models.MtgDraft import MtgDraft
from models.MtgDraftPackContent import MtgDraftPackContent
from models.MtgDraftPickWeight import MtgDraftPickWeight
from models.MtgEdition import MtgEdition
from models.MtgDraftPicks import MtgDraftPicks

@sql_logging
def getAllEditions():
    query = MtgEdition.query.filter_by(delete_flag=0)
    query = query.filter_by(is_booster=1)
    query = query.order_by(MtgEditionbooster_sort.desc())
    query = query.all()
    
    return query


