from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import City
from app.schemas import CityCreate, CityOut, CityUpdate

app = FastAPI(
    title="Cities API",
    description="CRUD API for global cities dataset",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/cities", response_model=CityOut, status_code=status.HTTP_201_CREATED)
def create_city(payload: CityCreate, db: Session = Depends(get_db)):
    existing = db.get(City, payload.station_id)
    if existing:
        raise HTTPException(status_code=409, detail="station_id already exists")

    city = City(**payload.model_dump())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


@app.get("/cities", response_model=list[CityOut])
def list_cities(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return db.query(City).offset(skip).limit(limit).all()


@app.get("/cities/{station_id}", response_model=CityOut)
def get_city(station_id: str, db: Session = Depends(get_db)):
    city = db.get(City, station_id)
    if not city:
        raise HTTPException(status_code=404, detail="city not found")
    return city


@app.put("/cities/{station_id}", response_model=CityOut)
def update_city(station_id: str, payload: CityUpdate, db: Session = Depends(get_db)):
    city = db.get(City, station_id)
    if not city:
        raise HTTPException(status_code=404, detail="city not found")

    for key, value in payload.model_dump().items():
        setattr(city, key, value)

    db.commit()
    db.refresh(city)
    return city


@app.delete("/cities/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(station_id: str, db: Session = Depends(get_db)):
    city = db.get(City, station_id)
    if not city:
        raise HTTPException(status_code=404, detail="city not found")

    db.delete(city)
    db.commit()
    return None
