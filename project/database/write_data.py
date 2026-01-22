from sqlmodel import Session, select
from .db import engine
from shemas.selery_app_shemas import RawIndexPrise, RawContractSise
from shemas.db_models import Stock, Index, IndexPrice





def write_index_price(raw_index_price: RawIndexPrise):
    with Session(engine) as session:
        st_st = select(Stock).where(Stock.name == raw_index_price.stock)
        
        try:
            st = session.exec(st_st).one()
        except Exception:
            st = Stock(name=raw_index_price.stock)
            session.add(st)
            session.commit()
            session.refresh(st)
        
        idx_st = select(Index).where(Index.name == raw_index_price.idx)
        try:
            idx = session.exec(idx_st).one()
        except Exception:
            idx = Index(name=raw_index_price.idx)
            session.add(idx)
            session.commit()
            session.refresh(idx)
        
        
        ind_p = IndexPrice(st_id=st.id, 
                           idx_id=idx.id, 
                           timestamp=raw_index_price.idx_prise_time,
                           prise=raw_index_price.idx_prise)
        session.add(ind_p)
        session.commit()