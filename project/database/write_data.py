from sqlmodel import Session, select
from .db import engine
from shemas.selery_app_shemas import RawIndexPrise, RawContractSise
from shemas.db_models import Stock, Index, IndexPrice, Ticker
from datetime import datetime


def _get_stock(stock_nam: str, session: Session) -> Stock:
    st_st = select(Stock).where(Stock.name == stock_nam)

    try:
        st = session.exec(st_st).one()
    except Exception:
        st = Stock(name=stock_nam)
        session.add(st)
        session.commit()
        session.refresh(st)
    return st


def _get_index(index_name: str, session: Session) -> Index:
    idx_st = select(Index).where(Index.name == index_name)

    try:
        idx = session.exec(idx_st).one()
    except Exception:
        idx = Index(name=index_name)
        session.add(idx)
        session.commit()
        session.refresh(idx)
    return idx


def _get_ticker(ticker_name: str, session: Session) -> Ticker:
    ti_st = select(Ticker).where(Ticker.name == ticker_name)

    try:
        ti = session.exec(ti_st).one()
    except Exception:
        ti = Ticker(name=ticker_name)
        session.add(ti)
        session.commit()
        session.refresh(ti)
    return ti


def _write_index_price(
    stock: Stock,
    index: Index,
    ticker: Ticker,
    dt: datetime,
    price: float,
    session: Session,
):
    ind_p = IndexPrice(
        st_id=stock.id, idx_id=index.id, tic_id=ticker.id, timestamp=dt, price=price
    )
    session.add(ind_p)
    session.commit()

def _write_index_price_from_raw(*,
        session: Session,
        stock: str,
        idx_prise: float,
        idx_prise_time: datetime,
        ticker: str, 
        index: str
    ):

    st = _get_stock(stock, session)
    idx = _get_index(index, session)
    ti = _get_ticker(ticker, session)

    _write_index_price(
        st,
        idx,
        ti,
        idx_prise_time,
        idx_prise,
        session,
    )

def write_index_price(raw_index_price: RawIndexPrise):
    stock = raw_index_price.stock
    idx_price = raw_index_price.idx_prise
    idx_price_time = raw_index_price.idx_prise_time
    ticker, index = raw_index_price.idx.split("_")

    with Session(engine) as session:
        _write_index_price_from_raw(session=session, 
                                    stock=stock, 
                                    idx_prise=idx_price, 
                                    idx_prise_time=idx_price_time,
                                    ticker=ticker, 
                                    index=index, )
        
