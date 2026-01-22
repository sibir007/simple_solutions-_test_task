
from datetime import datetime
from pydantic import BaseModel


class ResponseInem(BaseModel):
    stock: str
    ticker: str
    index: str
    price: float
    date: datetime


class RequestModel(BaseModel):
    stock: str
    ticker: str
    index: str
    dates: list[datetime]
