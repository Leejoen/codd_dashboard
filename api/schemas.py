from pydantic import BaseModel
from typing import Optional

# Для upload_csv не нужны схемы, так как файл передается напрямую

class ZoneRoadRequest(BaseModel):
    point_from: str
    point_to: str

class ZoneRoadResponse(BaseModel):
    zone: str
    road: str
    indexes: str

class CostRequest(BaseModel):
    road: str
    day_of_week: str
    time_range: str
    time_start: str
    time_end: str
    car_type: str
    zone: str
    transponder: str
    transponder_type: str
    tariff: str
    direction: str

class CostResponse(BaseModel):
    price: float
    postpay_time: int
