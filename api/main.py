from sqlalchemy.orm import Session
import pandas as pd
import io

from api import models, schemas, database
from .database import get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, WebSocketException

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники, измените на конкретные домены при необходимости
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц
models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# @app.post("/upload_csv/")
# async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     if not file.filename.endswith('.csv'):
#         raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

#     content = await file.read()
#     df = pd.read_csv(io.StringIO(content.decode("utf-8")))

#     # Проверка необходимых колонок
#     required_columns = {"point_from", "point_to", "zone", "road", "indexes"}
#     if not required_columns.issubset(df.columns):
#         raise HTTPException(status_code=400, detail="CSV must contain columns: point_from, point_to, zone, road, indexes")

#     # Запись данных в базу
#     for _, row in df.iterrows():
#         point_data = models.PointData(
#             point_from=row["point_from"],
#             point_to=row["point_to"],
#             zone=row["zone"],
#             road=row["road"],
#             indexes=row["indexes"]
#         )
#         db.add(point_data)

#     db.commit()
#     return {"status": "success", "message": "CSV data has been uploaded successfully"}

@app.post("/get_zone_road/", response_model=schemas.ZoneRoadResponse)
def get_zone_road(request: schemas.ZoneRoadRequest, db: Session = Depends(get_db)):
    record = db.query(models.PointData).filter(
        models.PointData.point_from == request.point_from,
        models.PointData.point_to == request.point_to
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Data not found for given points")

    return schemas.ZoneRoadResponse(zone=record.zone, road=record.road, indexes=record.indexes)

@app.post("/get_cost/", response_model=schemas.CostResponse)
def get_cost(request: schemas.CostRequest, db: Session = Depends(get_db)):
    record = db.query(models.Tariff).filter(
        models.Tariff.road == request.road,
        models.Tariff.day_of_week == request.day_of_week,
        models.Tariff.time_range == request.time_range,
        models.Tariff.time_start == request.time_start,
        models.Tariff.time_end == request.time_end,
        models.Tariff.car_type == request.car_type,
        models.Tariff.zone == request.zone,
        models.Tariff.transponder == request.transponder,
        models.Tariff.transponder_type == request.transponder_type,
        models.Tariff.tariff == request.tariff,
        models.Tariff.direction == request.direction
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Cost data not found for given parameters")

    return schemas.CostResponse(price=record.price, postpay_time=record.postpay_time)
