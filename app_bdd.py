"""Module working on app database"""

import re
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import relationship

from sqlalchemy.interfaces import PoolListener
class ForeignKeysListener(PoolListener):
    def connect(self, dbapi_con, con_record):
        db_cursor = dbapi_con.execute('pragma foreign_keys=ON')

#Create BDD
engine = create_engine("sqlite:///dairy.db", listeners=[ForeignKeysListener()]) #, isolation_level= "SERIALIZABLE")

#Create tables
Base = declarative_base()
class Dates(Base):
    __tablename__ = "dates"

    id = Column(Integer, primary_key=True)
    year_to_day = Column(Integer)
    hour = Column(String)
    label = Column(String)
    precipitation = Column(Float)
    address_id = Column(Integer, ForeignKey("addresses.id"))

    address = relationship("Addresses", back_populates="dates")

    def __repr__(self):
        return (f"<Dates (id= {self.id}, year_to_day= {self.year_to_day}, hour= {self.hour}, "
        f"label= {self.label}, precipitation= {self.precipitation}, address_id= {self.address_id})>")

class Addresses(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    num = Column(Integer)
    street = Column(String)
    zipcode = Column(Integer)
    city = Column(String)
    lat = Column(Float)
    lon = Column(Float)

    dates = relationship("Dates", order_by= Dates.id, back_populates="address")

    def __repr__(self):
        return f"<Addresses (id= {self.id}, num= {self.num}, street= {self.street}, "
        f"zipcode= {self.zipcode}, city= {self.city}, lat= {self.lat}, lon= {self.lon})>"

metadata = MetaData()
Base.metadata.create_all(engine)

from sqlalchemy.engine import Engine
Engine.connect(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
