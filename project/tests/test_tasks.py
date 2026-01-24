from fastapi import Response

# all prices for ticker by all indexes
def test_case1(client):
    response: Response = client.get("/deribit?ticker=btc") 
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 8640 # 3d*24h*60m*2index=8640rows
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp

# all prices for ticker by a specific index
def test_case2(client):
    response: Response = client.get("/deribit?ticker=btc&index=usd")
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 4320 # 3d*24h*60m*1index=4320rows
    assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp


# all prices for ticker by a specific index for a specified period of time
def test_case3(client):
    response: Response = client.get("/deribit?ticker=btc&index=usd&dates=2026-01-02T00:00:00.000000&dates=2026-01-02T23:58:59.999999")
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 1439 # ((1d*24h*60m)-1m)*1index=1439rows
    assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'ust', 'price': 1.0, 'date': '2026-01-02T23:59:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-02T23:58:00'} in resp

# all prices for ticker by a specific index for a specified day
def test_case4(client):
    response: Response = client.get("/deribit?ticker=btc&index=usd&dates=2026-01-02T23:58:59.9999")
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 1440 # 1d*24h*60m*1index=1440rows
    assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'ust', 'price': 1.0, 'date': '2026-01-02T00:00:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-02T17:20:00'} in resp

# all prices for ticker by all index for a specified period of time 
def test_case5(client):
    response: Response = client.get("/deribit?ticker=btc&dates=2026-01-02T00:00:00.000000&dates=2026-01-02T23:58:59.999999")
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 2878 # ((1d*24h*60m)-1m)*2index=2878rows
    assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'ust', 'price': 1.0, 'date': '2026-01-02T23:59:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-02T23:58:00'} in resp
    assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-02T23:59:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-02T23:58:00'} in resp

# all prices for ticker by all indexes for a specified day
def test_case6(client):
    response: Response = client.get("/deribit?ticker=btc&dates=2026-01-02T23:58:59.999999")
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 2880 # 1d*24h*60m*2index=2880rows
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-02T00:01:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-02T17:20:00'} in resp
    assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-03T00:00:00'} in resp
    assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-03T17:20:00'} in resp

# last price
def test_case7(client):
    response: Response = client.get("/deribit?ticker=btc&index=usd&dates=last")
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 1
    assert [{'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-03T23:59:00'}] == resp
