from pydantic import BaseModel
from datetime import datetime, timezone

class RawIndexPrise(BaseModel):
    stock: str
    idx: str
    idx_prise: float
    idx_prise_time: datetime

class RawContractSise(BaseModel):
    stock: str
    contract_size: int