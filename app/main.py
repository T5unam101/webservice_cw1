from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import City, Country
from app.schemas import (
    CityCreate,
    CityOut,
    CityUpdate,
    CountryCreate,
    CountryOut,
    CountryUpdate,
)

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


@app.get("/cities/by-latitude", response_model=list[CityOut])
def list_cities_by_latitude(
    limit: int = Query(default=20, ge=1, le=300),
    db: Session = Depends(get_db),
):
    # Higher latitude means closer to the North Pole.
    return db.query(City).order_by(City.latitude.desc()).limit(limit).all()


@app.get("/cities/nearest")
def nearest_city(
    city_name: str = Query(..., min_length=1),
    iso2: str | None = Query(default=None, min_length=2, max_length=2),
    db: Session = Depends(get_db),
):
    source_query = db.query(City).filter(func.lower(City.city_name) == city_name.lower())
    if iso2:
        source_query = source_query.filter(func.lower(City.iso2) == iso2.lower())

    source_candidates = source_query.limit(2).all()
    if not source_candidates:
        raise HTTPException(status_code=404, detail="source city not found")
    if len(source_candidates) > 1 and not iso2:
        raise HTTPException(
            status_code=409,
            detail="multiple cities found, please provide iso2 to disambiguate",
        )

    source_city = source_candidates[0]

    # Haversine formula in SQL to compute distance (km) from source city.
    distance_expr = 6371 * func.acos(
        func.cos(func.radians(source_city.latitude))
        * func.cos(func.radians(City.latitude))
        * func.cos(func.radians(City.longitude) - func.radians(source_city.longitude))
        + func.sin(func.radians(source_city.latitude)) * func.sin(func.radians(City.latitude))
    )

    row = (
        db.query(City, distance_expr.label("distance_km"))
        .filter(City.station_id != source_city.station_id)
        .order_by(distance_expr.asc())
        .limit(1)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="no city data found")

    city, distance_km = row
    return {
        "query": {"city_name": city_name, "iso2": iso2},
        "source_city": {
            "station_id": source_city.station_id,
            "city_name": source_city.city_name,
            "country": source_city.country,
            "state": source_city.state,
            "iso2": source_city.iso2,
            "iso3": source_city.iso3,
            "latitude": float(source_city.latitude),
            "longitude": float(source_city.longitude),
        },
        "nearest_city": {
            "station_id": city.station_id,
            "city_name": city.city_name,
            "country": city.country,
            "state": city.state,
            "iso2": city.iso2,
            "iso3": city.iso3,
            "latitude": float(city.latitude),
            "longitude": float(city.longitude),
        },
        "distance_km": round(float(distance_km), 3),
    }


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


@app.post("/countries", response_model=CountryOut, status_code=status.HTTP_201_CREATED)
def create_country(payload: CountryCreate, db: Session = Depends(get_db)):
    existing = db.get(Country, payload.iso2)
    if existing:
        raise HTTPException(status_code=409, detail="iso2 already exists")

    country = Country(**payload.model_dump())
    db.add(country)
    db.commit()
    db.refresh(country)
    return country


@app.get("/countries", response_model=list[CountryOut])
def list_countries(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=300),
    continent: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Country)
    if continent:
        query = query.filter(Country.continent == continent)
    return query.order_by(Country.country).offset(skip).limit(limit).all()


@app.get("/countries/{iso2}", response_model=CountryOut)
def get_country(iso2: str, db: Session = Depends(get_db)):
    country = db.get(Country, iso2)
    if not country:
        raise HTTPException(status_code=404, detail="country not found")
    return country


@app.put("/countries/{iso2}", response_model=CountryOut)
def update_country(iso2: str, payload: CountryUpdate, db: Session = Depends(get_db)):
    country = db.get(Country, iso2)
    if not country:
        raise HTTPException(status_code=404, detail="country not found")

    for key, value in payload.model_dump().items():
        setattr(country, key, value)

    db.commit()
    db.refresh(country)
    return country


@app.delete("/countries/{iso2}", status_code=status.HTTP_204_NO_CONTENT)
def delete_country(iso2: str, db: Session = Depends(get_db)):
    country = db.get(Country, iso2)
    if not country:
        raise HTTPException(status_code=404, detail="country not found")
    db.delete(country)
    db.commit()
    return None


@app.get("/analytics/cities-per-country")
def cities_per_country(limit: int = Query(default=10, ge=1, le=100), db: Session = Depends(get_db)):
    rows = (
        db.query(
            Country.iso2,
            Country.country,
            func.count(City.station_id).label("city_count"),
        )
        .join(City, City.iso2 == Country.iso2)
        .group_by(Country.iso2, Country.country)
        .order_by(func.count(City.station_id).desc())
        .limit(limit)
        .all()
    )
    return [
        {"iso2": row.iso2, "country": row.country, "city_count": int(row.city_count)}
        for row in rows
    ]


@app.get("/analytics/countries-by-continent")
def countries_by_continent(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Country.continent,
            func.count(Country.iso2).label("country_count"),
        )
        .group_by(Country.continent)
        .order_by(func.count(Country.iso2).desc())
        .all()
    )
    return [
        {"continent": row.continent or "Unknown", "country_count": int(row.country_count)}
        for row in rows
    ]
