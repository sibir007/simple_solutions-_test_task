from sqlmodel import Session, select
from .db import engine
from shemas.selery_app_shemas import RawIndexPrise, RawContractSise
from shemas.db_models import Stock, Index, IndexPrice, Ticker
from datetime import datetime


def _select_st():
    return (
            select(
                Stock.name,
                Ticker.name,
                Index.name,
                IndexPrice.price,
                IndexPrice.timestamp,
            )
            .join(Stock)
            .join(Ticker)
            .join(Index)
        )

def _pack_to_dict_list(tuple_list):
    return [{"stock": stock, "ticker": ticker, "index": index, "price": price,  "date": dates} for 
                          stock, ticker, index, price, dates in tuple_list]

def _get_index_case_1(stock, ticker):
    with Session(engine) as s:
        select_st_where = _select_st()\
            .where(Stock.name == stock)\
                .where(Ticker.name == ticker)
        res_rows = s.exec(select_st_where).all()
    return _pack_to_dict_list(res_rows)
    
def _get_index_case_2(stock, ticker, index):
    with Session(engine) as s:
        select_st_where = _select_st()\
            .where(Stock.name == stock)\
                .where(Ticker.name == ticker)\
                    .where(Index.name == index)
        res_rows = s.exec(select_st_where).all()
    return _pack_to_dict_list(res_rows)

def _get_index_case_3(stock:str, ticker:str, index:str, dates: list[datetime]):
    assert len(dates) == 2
    dates.sort()
    with Session(engine) as s:
        select_st_where = _select_st()\
            .where(Stock.name == stock)\
                .where(Ticker.name == ticker)\
                    .where(Index.name == index)\
                        .where(IndexPrice.timestamp >= dates[0])\
                            .where(IndexPrice.timestamp < dates[1])
        res_rows = s.exec(select_st_where).all()
    return _pack_to_dict_list(res_rows)

def _get_index_case_4(stock, ticker, index, date: datetime):
    d1 = date.replace(hour=0,minute=0,second=0,microsecond=0)
    d2 = d1.replace(hour=23,minute=59,second=59,microsecond=999999)
    return _get_index_case_3(stock, ticker, index, [d1,d2])


def _get_index_case_5(stock:str, ticker:str, dates: list[datetime]):
    assert len(dates) == 2
    dates.sort()
    with Session(engine) as s:
        select_st_where = _select_st()\
            .where(Stock.name == stock)\
                .where(Ticker.name == ticker)\
                        .where(IndexPrice.timestamp >= dates[0])\
                            .where(IndexPrice.timestamp < dates[1])
        res_rows = s.exec(select_st_where).all()
    return _pack_to_dict_list(res_rows)

def _get_index_case_6(stock, ticker, date: datetime):
    d1 = date.replace(hour=0,minute=0,second=0,microsecond=0)
    d2 = d1.replace(hour=23,minute=59,second=59,microsecond=999999)
    return _get_index_case_5(stock, ticker, [d1,d2])


def get_trick_index_info(request):
    match request:
        # case_1 client.get("/deribit?ticker=btc")
        case {"stock": stock, "ticker": ticker, "index": None, "dates": None}:
            return _get_index_case_1(stock, ticker)
        # case_2 client.get("/deribit?ticker=btc&index=usd")
        case {"stock": stock, "ticker": ticker, "index": index, "dates": None}:
            return _get_index_case_2(stock, ticker, index)
        case {"stock": stock, "ticker": ticker, "index": None, "dates": dates}:
            match dates:
                # case_5 client.get("/deribit?ticker=btc&dates=2026-01-02T00:00:00.000000&dates=2026-01-02T23:58:59.999999")
                case [_, _]:
                    return _get_index_case_5(stock, ticker, dates)
                # case_6
                case [date]:
                    return _get_index_case_6(stock, ticker, date)
        case {"stock": stock, "ticker": ticker, "index": index, "dates": dates}:
            match dates:
                # case_3 client.get("/deribit?ticker=btc&index=usd&dates=2026-01-02T00:00:00.000000&dates=2026-01-02T23:59:59.999999")
                case [_, _]:
                    
                    return _get_index_case_3(stock, ticker, index, dates) 
                # case_4 client.get("/deribit?ticker=btc&index=usd&dates=2026-01-02T23:58:59.999999")
                case [date]:
                    return _get_index_case_4(stock, ticker, index, date) 
        
        case _:
            return [{"stock": None, "ticker": None, "index": None, "dates": None}]

    # with Session(engine) as session:

