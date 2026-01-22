from sqlmodel import Session, select
from .db import engine
from shemas.selery_app_shemas import RawIndexPrise, RawContractSise
from shemas.db_models import Stock, Index, IndexPrice, Ticker
from datetime import datetime
from shemas.fastapi_app_shemas import ResponseInem, RequestModel


def get_trick_index_info(req: RequestModel) -> list[ResponseInem]:
    pass