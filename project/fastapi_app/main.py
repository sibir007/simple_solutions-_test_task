from datetime import datetime
from typing import Annotated, Literal
from fastapi import FastAPI, Path, Query
from database.read_data import get_trick_index_info


app = FastAPI()
# app.mount("/static", StaticFiles(directory="fastapi_app/static"), name="static")
# test_templates = Jinja2Templates(directory="fastapi_app/templates")


@app.get("/{stock}")
async def get_index_price(
    stock: Annotated[
        Literal["deribit", "somestock"],
        Path(title="Stock", description="Stock for request"),
    ],
    ticker: Annotated[
        Literal["btc", "eth"], Query(title="Ticker", description="Ticker for request")
    ],
    index: Annotated[
        Literal["usd", "eurr"] | None,
        Query(title="Index", description="Index for request"),
    ] = None,
    dates: Annotated[
        list[datetime] | list[Literal["last"]] | None,
        Query(title="Dates", description="""Dates for request. 
              If [datetime]: Selection by the specified date. 
              If [datetime, datetime]: selection for the time period. 
              If ["last"]: latest price. 
              If None: selection for the entire time (without pagination)"""
              , max_length=2),
    ] = None,
):
    
    query_items = get_trick_index_info({"stock":stock, "ticker":ticker, "index":index, "dates":dates})
    return query_items

