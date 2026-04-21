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
