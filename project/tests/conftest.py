import pytest
from starlette.testclient import TestClient
from datetime import datetime, timedelta
from shemas.db_models import Stock, Index, Ticker, IndexPrice



@pytest.fixture(scope="module")
def test_app():
    from fastapi_app import app
    client = TestClient(app)
    yield client 


@pytest.fixture(scope="module")
def test_db_session():
    
    from dotenv import load_dotenv
    load_dotenv()
    
    import os
    os.environ["APP_CONFIG"] = "test"

    from database.db import init_db, engine
    from sqlmodel import Session
    with Session(engine) as s:
        init_db()
        t1 = Ticker(id=1, name="btc")
        t2 = Ticker(id=2, name="eth")
        i1 = Index(id=1,name="usd")
        i2 = Index(id=2,name="eurr")
        s1 = Stock(id=1, name="deribit")
        s2 =  Stock(id=2,name="somestock")
        s.add(t1)
        s.add(t1)
        s.add(i1)
        s.add(i2)
        s.add(s1)
        s.add(s2)

        start_dt = datetime(2026,1,1)
        for min in range(3*24*60): # 3 days
            # 4320 min: 
            # 2026-01-01 00:00:00 - 2026-01-03 23:59:00 
            td = timedelta(minutes=min)
            dt = start_dt + td

            # stock 1
            ip1 = IndexPrice(st_id=s1.id,
                             tic_id=t1.id,
                             idx_id=i1.id,
                             timestamp=dt,
                             price=1.0)
            ip2 = IndexPrice(st_id=s1.id,
                             tic_id=t1.id,
                             idx_id=i2.id,
                             timestamp=dt,
                             price=1.0)
            ip3 = IndexPrice(st_id=s1.id,
                             tic_id=t2.id,
                             idx_id=i1.id,
                             timestamp=dt,
                             price=1.0)
            ip4 = IndexPrice(st_id=s1.id,
                             tic_id=t2.id,
                             idx_id=i2.id,
                             timestamp=dt,
                             price=1.0)
            # stock 2
            ip5 = IndexPrice(st_id=s2.id,
                             tic_id=t1.id,
                             idx_id=i1.id,
                             timestamp=dt,
                             price=1.0)
            ip6 = IndexPrice(st_id=s2.id,
                             tic_id=t1.id,
                             idx_id=i2.id,
                             timestamp=dt,
                             price=1.0)
            ip7 = IndexPrice(st_id=s2.id,
                             tic_id=t2.id,
                             idx_id=i1.id,
                             timestamp=dt,
                             price=1.0)
            ip8 = IndexPrice(st_id=s2.id,
                             tic_id=t2.id,
                             idx_id=i2.id,
                             timestamp=dt,
                             price=1.0)

            s.add(ip1)
            s.add(ip2)
            s.add(ip3)
            s.add(ip4)
            s.add(ip5)
            s.add(ip6)
            s.add(ip7)
            s.add(ip8)
        s.commit()
        yield s





