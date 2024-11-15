from .database import Base
from sqlalchemy import Column, Integer, String, Float


class PointData(Base):
    __tablename__ = "points_data"

   
    point_from = Column(String, index=True)
    point_to = Column(String, index=True)
    zone = Column(String)
    road = Column(String)
    indexes = Column(String)

class Tariff(Base):
    __tablename__ = "tariffs"

    road = Column(String, index=True)
    day_of_week = Column(String, index=True)
    time_range = Column(String, index=True)
    time_start = Column(String)
    time_end = Column(String)
    car_type = Column(String)
    zone = Column(String)
    transponder = Column(String)
    transponder_type = Column(String)
    tariff = Column(String)
    direction = Column(String)
    price = Column(Float)
    postpay_time = Column(Integer)
