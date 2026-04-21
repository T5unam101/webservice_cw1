from pydantic import BaseModel, Field


class CityBase(BaseModel):
    city_name: str = Field(..., max_length=128)
    country: str = Field(..., max_length=128)
    state: str = Field(..., max_length=128)
    iso2: str = Field(..., min_length=2, max_length=2)
    iso3: str = Field(..., min_length=3, max_length=3)
    latitude: float
    longitude: float


class CityCreate(CityBase):
    station_id: str = Field(..., max_length=16)


class CityUpdate(CityBase):
    pass


class CityOut(CityBase):
    station_id: str

    class Config:
        from_attributes = True
