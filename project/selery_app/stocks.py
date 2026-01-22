from datetime import datetime, timezone
import requests
import inspect
from  shemas.selery_app_shemas import RawIndexPrise, RawContractSise


class NoInstances(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("Can't instantiate directly")

class StockBase(metaclass=NoInstances):

    _stock_name = "stockbase"

    @classmethod
    def call_api_one(cls, stock_name: str, api_name: str, **kw):
        clss_met = cls._get_one_sub_class_met_by_stock_name(stock_name, api_name)
        if not clss_met:
            raise ValueError(f"api: {api_name} for stock {stock_name} not found")
        
        return clss_met[1](**kw)
    
    # @classmethod
    # def call_api_all(cls, api_name: str, **kw):
    #     sub_clss_met = cls._get_all_sub_class_met_by_met_name(api_name)
    #     if not sub_clss_met:
    #         raise ValueError(f"api: {api_name} not found")
    #     for cls_met in sub_clss_met:
    #         cls_met[1](**kw)
    #     return


    @classmethod
    def _get_one_sub_class_met_by_stock_name(cls, stock_name: str, met_name: str):
        sub_clss_met = cls._get_all_sub_class_met_by_met_name(met_name)
        for scls_met in sub_clss_met:
            if scls_met[0]._get_stock_name() == stock_name:
                return scls_met
        return []


    @classmethod
    def _get_all_sub_class_met_by_met_name(cls, method_name):
        sub_clss = cls._all_subclasses()
        sub_clss_met = []
        for cls_ in sub_clss:
            for met in inspect.getmembers(cls_, predicate=inspect.ismethod):
                if met[0] == method_name:
                    sub_clss_met.append([cls_, met[1]])
                    break
        return sub_clss_met
        

    @classmethod
    def _all_subclasses(cls):
        return (sub_cls for sub_cls in cls.__subclasses__())

    @classmethod
    def _get_stock_name(cls) -> str:
        return cls._stock_name

    @classmethod
    def get_contract_size(cls) -> RawContractSise:
        pass

    @classmethod
    def get_index_price(cls, index_name: str) -> RawIndexPrise:
        pass



class SomeStock(StockBase):
    _stock_name = "somestock"

    # TODO: implement
    @classmethod
    def get_index_price(cls, index_name: str) -> RawIndexPrise:
        raise NotImplementedError("NotImplementedError")

class DeriBit(StockBase):

    _stock_name = "deribit"

    @classmethod
    def get_index_price(cls, index_name: str) -> RawIndexPrise:
        # True case
        # {
        #   "jsonrpc": "2.0",
        #   "result": {
        #     "estimated_delivery_price": 90999.22,
        #     "index_price": 90999.22
        #   },
        #   "usIn": 1768916400505372,
        #   "usOut": 1768916400505576,
        #   "usDiff": 204,
        #   "testnet": true
        # }
        connect_timeout, read_timeout = 5.0, 30.0
        url = f"https://test.deribit.com/api/v2/public/get_index_price?index_name={index_name}"
        
        response = requests.get(url, timeout=(connect_timeout, read_timeout))
        match response.json():
            case {"result": { "index_price": prise}}:
                return RawIndexPrise(stock=cls._get_stock_name(), 
                                idx=index_name, 
                                idx_prise=prise,
                                # idx_prise=float(rez.get("index_price")),
                                idx_prise_time=datetime.now(tz=timezone.utc))
            case _ :
                raise requests.RequestException(response.text)
                
                

if __name__ == '__main__':
    print("call true deribit_index_price")
    res = StockBase.call_api_one('deribit', 'get_index_price', index_name='btc_usd')
    print(res)
    print("call false deribit_index_price")
    try:
        StockBase.call_api_one('deribit', 'get_index_price', index_name='false_idx')
    except Exception as e:
        print(e)
    try:
        StockBase.call_api_one('somestock', 'get_index_price', index_name='btc_usd')

    except Exception as e:
        print(e)

