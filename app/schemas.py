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


class CountryBase(BaseModel):
    country: str = Field(..., max_length=128)
    native_name: str | None = Field(default=None, max_length=255)
    iso3: str = Field(..., min_length=3, max_length=3)
    population: float | None = None
    area: float | None = None
    capital: str | None = Field(default=None, max_length=128)
    capital_lat: float | None = None
    capital_lng: float | None = None
    region: str | None = Field(default=None, max_length=128)
    continent: str | None = Field(default=None, max_length=64)


class CountryCreate(CountryBase):
    iso2: str = Field(..., min_length=2, max_length=2)


class CountryUpdate(CountryBase):
    pass


class CountryOut(CountryBase):
    iso2: str

    class Config:
        from_attributes = True
