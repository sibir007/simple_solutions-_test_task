
from sqlmodel import create_engine, SQLModel, Session
from shemas import db_models
import datetime

from config import get_settings

DATABASE_URL = get_settings().DATABASE_URL

print(f"---------------------{DATABASE_URL}-------------------")
# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session


def create_db():
    SQLModel.metadata.create_all(engine)

def init_db_with_start_value():
    create_db() # if db not exist
    drop_db()
    create_db()
    # with Session(engine) as session:

    #     exch1 = db_models.Stock(name="binance")
    #     exch2 = db_models.Stock(name="deribit")
        
    #     ix1 = db_models.Index(name="btc_usd")
    #     ix2 = db_models.Index(name="eth_usd")
        
    #     session.add(exch1)
    #     session.add(exch2)
    #     session.add(ix1)
    #     session.add(ix2)
        
    #     session.commit()


def drop_db():
    SQLModel.metadata.drop_all(engine)


def fill_db_start_data():
    with Session(engine) as session:

        exch1 = db_models.Stock(name="Binance")
        exch2 = db_models.Stock(name="Upbit")
        
        ix1 = db_models.Index(name="aaa")
        ix2 = db_models.Index(name="bbb")
        ix3 = db_models.Index(name="ccc")
        
        session.add(exch1)
        session.add(exch2)
        session.add(ix1)
        session.add(ix2)
        session.add(ix3)
        
        session.commit()

        ip1 = db_models.IndexPrice(
            st_id=exch1.id,
            idx_id=ix1.id,
            timestamp=datetime.datetime.now(),
            prise=1.1,
        )
        ip2 = db_models.IndexPrice(
            st_id=exch1.id,
            idx_id=ix2.id,
            timestamp=datetime.datetime.now(),
            prise=1.2,
        )
        ip3 = db_models.IndexPrice(
            st_id=exch1.id,
            idx_id=ix3.id,
            timestamp=datetime.datetime.now(),
            prise=1.3,
        )
        ip4 = db_models.IndexPrice(
            st_id=exch2.id,
            idx_id=ix1.id,
            timestamp=datetime.datetime.now(),
            prise=2.1,
        )
        ip5 = db_models.IndexPrice(
            st_id=exch2.id,
            idx_id=ix2.id,
            timestamp=datetime.datetime.now(),
            prise=2.2,
        )

        session.add(ip1)
        session.add(ip2)
        session.add(ip3)
        session.add(ip4)
        session.add(ip5)

        session.commit()


def main():
    drop_db()
    create_db()
    fill_db_start_data()
    main()





