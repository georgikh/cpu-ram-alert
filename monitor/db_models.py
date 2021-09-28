# This Python file uses the following encoding: utf-8

from sqlalchemy import Column, Integer, Float, String, DateTime, Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import datetime
import enum

Base = declarative_base()

db_name = 'alertdb'
db_user = 'someuser'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)

engine = create_engine(db_string, echo=True)

class Alert_type(enum.Enum):
    ram = 1
    cpu = 2
    
class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key = True)
    hostname = Column(String)
    alert_type = Column(Enum(Alert_type))
    average_percent = Column(Float)
    current_percent = Column(Float)
    high_use_time = Column(Float)
    interval = Column(Float)
    createdAt = Column(DateTime,default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)
