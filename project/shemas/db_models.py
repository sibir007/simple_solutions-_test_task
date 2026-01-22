from sqlmodel import SQLModel, Field
from datetime import datetime, date, time, timezone
from .selery_app_shemas import RawIndexPrise


class Stock(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Index(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Ticker(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class IndexPrice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    st_id: int = Field(foreign_key="stock.id")
    tic_id: int = Field(foreign_key="ticker.id")
    idx_id: int = Field(foreign_key="index.id")
    timestamp: datetime = Field(nullable=False)
    price: float = Field(nullable=False)
