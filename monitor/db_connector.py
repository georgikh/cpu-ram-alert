# This Python file uses the following encoding: utf-8

import db_models as models
from sqlalchemy.orm import sessionmaker

class DB_Controller:
    def __init__(self,engine):
        self.engine = engine
        Session = sessionmaker(bind = self.engine)
        self.session = Session()

    def addRecord(self,record):
        self.session.add(record)
        self.session.commit()


    def addLogRecord(self,log):
        l = models.Log(
            hostname=log.hostname,
            alert_type=log.alert_type,
            average_percent = log.average_percent,
            current_percent = log.current_percent,
            high_use_time = log.high_use_time,
            interval = log.interval
        )
        self.addRecord(l)
