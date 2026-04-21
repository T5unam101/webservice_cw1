from sqlalchemy import DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    station_id: Mapped[str] = mapped_column(String(16), primary_key=True, index=True)
    city_name: Mapped[str] = mapped_column(String(128), nullable=False)
    country: Mapped[str] = mapped_column(String(128), nullable=False)
    state: Mapped[str] = mapped_column(String(128), nullable=False)
    iso2: Mapped[str] = mapped_column(String(2), nullable=False)
    iso3: Mapped[str] = mapped_column(String(3), nullable=False)
    latitude: Mapped[float] = mapped_column(DECIMAL(10, 7), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(10, 7), nullable=False)


class Country(Base):
    __tablename__ = "countries"

    iso2: Mapped[str] = mapped_column(String(2), primary_key=True, index=True)
    country: Mapped[str] = mapped_column(String(128), nullable=False)
    native_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    iso3: Mapped[str] = mapped_column(String(3), nullable=False)
    population: Mapped[float | None] = mapped_column(DECIMAL(16, 2), nullable=True)
    area: Mapped[float | None] = mapped_column(DECIMAL(16, 2), nullable=True)
    capital: Mapped[str | None] = mapped_column(String(128), nullable=True)
    capital_lat: Mapped[float | None] = mapped_column(DECIMAL(10, 6), nullable=True)
    capital_lng: Mapped[float | None] = mapped_column(DECIMAL(10, 6), nullable=True)
    region: Mapped[str | None] = mapped_column(String(128), nullable=True)
    continent: Mapped[str | None] = mapped_column(String(64), nullable=True)
