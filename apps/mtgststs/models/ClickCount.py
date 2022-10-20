# -*- encoding:utf8 -*-
from models.ModelManager import DB

class ClickCount(DB.Model):
    __tablename__ = 'click_count'
    __bind_key__ = 'log'
    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    href        = DB.Column(DB.Text(), nullable=False)
    count       = DB.Column(DB.Integer, nullable=False)
    type        = DB.Column(DB.Integer, nullable=False)
    delete_flag = DB.Column(DB.Integer, nullable=False)
    
    def __repr__(self):
        return "<ClickCount(id='%s', href='%s', count='%s',  type ='%s', delete_flag='%s')>" % (
            self.id, self.href, self.count, self.type, self.delete_flag)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'href'          : self.href,
            'count'         : self.count,
            'type'          : self.type,
            'delete_flag'   : self.delete_flag
        }