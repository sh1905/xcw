#!/usr/bin/env python
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,String,Integer,Float,Date
from sqlalchemy.ext.declarative import declarative_base
# 创建与数据库的连接
engine = create_engine('mysql+pymysql://xcw:182562@localhost:3306/sqlalchemy')
Base = declarative_base(bind=engine)#创建模型的基础类
Session =sessionmaker(bind=engine)

class User(Base):
    '''User模型'''
    __tablename__ = 'user' #创建模型对应的表名
    # 定义字段
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(20),unique=True)
    birthday = Column(Date)
    money = Column(Float, default=0.0)

Base.metadata.create_all()
session = Session()
bob = User(name='bob',birthday=datetime.date(1992,10,1),money=200)
tom = User(name='tom',birthday=datetime.date(1990,1,1),money=999)
lucy = User(name='lucy',birthday=datetime.date(1997,9,18),money=19)
jack = User(name='jack',birthday=datetime.date(1998,5,5),money=1)
eva = User(name='eva',birthday=datetime.date(1999,9,9))
alex = User(name='alex',birthday=datetime.date(2000,2,2),money=9.9)

session.add_all([bob,tom,lucy,jack,eva,alex])
session.commit()
