# -*- encoding:utf8 -*-
from models.ModelManager import DB

class Country(DB.Model):
    __tablename__ = 'country'
    __bind_key__ = 'info'
    id           = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    prefix       = DB.Column(DB.Text(), nullable=False)
    flag_prefix  = DB.Column(DB.Text(), nullable=True)
    name_en      = DB.Column(DB.Text(), nullable=False)
    name_jp      = DB.Column(DB.Text(), nullable=False)
    delete_flag  = DB.Column(DB.Integer, nullable=False)
    
    def __repr__(self):
        return "<Country(id='%s', prefix='%s', flag_prefix='%s',  name_en='%s',  name_jp='%s',  delete_flag='%s')>" % (
            self.id, self.prefix, self.flag_prefix, self.name_en, self.name_jp, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'           : self.id,
            'prefix'       : self.prefix,
            'flag_prefix'  : self.flag_prefix,
            'name_en'      : self.name_en,
            'name_jp'      : self.name_jp,
            'delete_flag'  : self.delete_flag
        }