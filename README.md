# simple_solutions_test_task

## SRS

1. Написать клиент для криптобиржи Deribit (https://docs.deribit.com/). Клиент должен каждую минуту забирать с биржи текущую цену btc_usd и eth_usd (index price валюты) после чего сохранять в базу данных тикер валюты, текущую цену и время в UNIX timestamp.

**Выполнено:**

**Celery worker задача:**
```py
# simple_solutions_test_task/project/selery_app/tasks.py
...
@app.task
def get_index_price(index_name: str):

    try:
        raw_index_price = StockBase.call_api_one('deribit', 'get_index_price', index_name=index_name)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False
    
    write_index_price(raw_index_price)
    return True
...
```
**Celery beat периодизация:**
```py
# simple_solutions_test_task/project/selery_app/tasks.py
...

@app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(60.0, get_index_price.s('btc_usd'), name='get_price_btc_usd')
    sender.add_periodic_task(60.0, get_index_price.s('eth_usd'), name='get_price_eth_usd')
    sender.add_periodic_task(60.0, get_index_price.s('btc_eurr'), name='get_price_btc_eurr')
    sender.add_periodic_task(60.0, get_index_price.s('eth_eurr'), name='get_price_eth_eurr')
...
```

2. Написать внешнее API для обработки сохраненных данных на FastAPI.

**Выполнено**

**Fastapi app:**
```py
# simple_solutions_test_task/project/fastapi_app/main/py
...

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

...

```

Обязательные требования:
1. API должно включать в себя следующие методы:

***Выполнено одним методом (entrypoint)***

- Получение всех сохраненных данных по указанной валюте
```py
# simple_solutions_test_task/project/tests/test_tasks.py
...
# all prices for ticker by all indexes
def test_case1(client):
    response: Response = client.get("/deribit?ticker=btc") 
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 8640 # 3d*24h*60m*2index=8640rows
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
...
```
- Получение последней цены валюты
```py
# simple_solutions_test_task/project/tests/test_tasks.py

# last price
...
def test_case7(client):
    response: Response = client.get("/deribit?ticker=btc&index=usd&dates=last")
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 1
    assert [{'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-03T23:59:00'}] == resp
...
```

- Получение цены валюты с фильтром по дате
```py
# simple_solutions_test_task/project/tests/test_tasks.py
...
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
...
```

Все методы должны быть GET и у каждого метода должен быть обязательный query-параметр “ticker”.

**Реализовано. Один GET метод для 7-ми юзкейсов**


2. В качестве БД использовать PostgreSQL.

**Выполнено:**

```yml
# simple_solutions_test_task/compose_db.yml

services:

  db:
    image: postgres
    container_name: postgres_db
    restart: always
    # set shared memory limit when using docker compose
    shm_size: 128mb
    # or set shared memory limit when deploy via swarm stack
    #volumes:
    #  - type: tmpfs
    #    target: /dev/shm
    #    tmpfs:
    #      size: 134217728 # 128*2^20 bytes = 128Mb
    environment:
      POSTGRES_USER: sibir
      POSTGRES_PASSWORD: sibirpass
      POSTGRES_DB: selery_app
      PGDATA: /var/lib/postgresql/data/pgdata    
    ports:
      - "5430:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data/pgdata
  adminer:
    image: adminer
    restart: always
    ports:
      - 8090:8080

volumes:
  pgdata:
    driver: local
```
3. Код выложить на gitlab с подробным readme и документацией по разворачиванию. В readme добавить секцию Design decisions.

**Выполнено**

4. Для периодического получения цен использовать Celery.

**Выполнено**

Необязательные требования:
1. Написать unit тесты для основных методов

**Выполнено**

7 тестов для `@app.get("/{stock}")` 

```bash
# simple_solutions_test_task/project/tests/test_tasks.py
(.venv) sibir007@sibir007:~/repos/simple_solutions_test_task/project$ python3 -m pytest 
========================================== test session starts ==========================================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/sibir007/repos/simple_solutions_test_task/project
plugins: anyio-4.12.1
collected 7 items                                                                                       

tests/test_tasks.py .......                                                                       [100%]

=========================================== warnings summary ============================================
../.venv/lib/python3.12/site-packages/_pytest/cacheprovider.py:475
  /home/sibir007/repos/simple_solutions_test_task/.venv/lib/python3.12/site-packages/_pytest/cacheprovider.py:475: PytestCacheWarning: cache could not write path /home/sibir007/repos/simple_solutions_test_task/project/.pytest_cache/v/cache/nodeids: [Errno 13] Permission denied: '/home/sibir007/repos/simple_solutions_test_task/project/.pytest_cache/v/cache/nodeids'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
===================================== 7 passed, 1 warning in 0.66s ======================================

```
2. Развернуть приложение в двух контейнерах для приложения и базы данных. 

**Выполнено**

`simple_solutions_test_task/compose_app.yml`

`simple_solutions_test_task/compose_db.yml`

```docker
# simple_solutions_test_task/project/Dockerfile

# pull official base image
FROM python:3.11.2-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

```

3. Применить aiohttp при написании клиента.

**Невыполнено**

## Architecture


![Software architecture](readme/arch.svg)


## DESIGN DECISION

### Progect directory structure

```bash
(.venv) sibir007@sibir007:~/repos/simple_solutions_test_task$ tree -L 2
.
├── compose_app.yml        # run fastapi selery app containers
├── compose_db.yml         # run db container
├── expample_env           # .env
├── LICENSE                
├── pgdata                 # db data
├── project
│   ├── alembic            # migration (no used now)
│   ├── alembic.ini
│   ├── config.py          # fastapi selery apps configuration
│   ├── database           # shared db logic
│   ├── Dockerfile         # fastapi selery apps containers
│   ├── fastapi_app        # fastapi app logic
│   ├── init_db.py         # init db script
│   ├── logs               # apps logs
│   ├── requirements.txt         
│   ├── selery_app         # shared selery apps logic
│   ├── shemas             # shred data models and schemas
│   ├── test_database.db   # test db, created when runnig tests
│   └── tests              # tests
├── readme                 # pictures for README.md
├── README_dev.md          # help when develop
└── README.md
```

### Design

![DESIGN DECISION](readme/des4.svg)


## DEPLOYMENT

### DB HOST
#### clone git repos
```bash
sibir007@sibir007:~/repos/deploy/db$ git clone https://github.com/sibir007/simple_solutions_test_task.git
Cloning into 'simple_solutions_test_task'...
remote: Enumerating objects: 292, done.
remote: Counting objects: 100% (292/292), done.
remote: Compressing objects: 100% (204/204), done.
remote: Total 292 (delta 169), reused 204 (delta 84), pack-reused 0 (from 0)
Receiving objects: 100% (292/292), 265.01 KiB | 1.05 MiB/s, done.
Resolving deltas: 100% (169/169), done.
sibir007@sibir007:~/repos/deploy/db$ cd simple_solutions_test_task/
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$ ls
compose_app.yml  expample_env  pgdata   readme         README.md
compose_db.yml   LICENSE       project  README_dev.md
```
#### create .env file
```bash
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$ mv expample_env .env
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$
```
#### create db store dir 
```bash
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$ mkdir pgdata
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$
```
#### run db container
```bash
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$ sudo docker compose -f  compose_db.yml  up -d
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task/project$ sudo docker ps
CONTAINER ID   IMAGE      COMMAND                  CREATED         STATUS         PORTS                                         NAMES
bcd8915ddb0a   adminer    "entrypoint.sh docke…"   4 minutes ago   Up 4 minutes   0.0.0.0:8090->8080/tcp, [::]:8090->8080/tcp   simple_solutions_test_task-adminer-1
52266a762db1   postgres   "docker-entrypoint.s…"   4 minutes ago   Up 4 minutes   0.0.0.0:5430->5432/tcp, [::]:5430->5432/tcp   postgres_db
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task/project$
```
#### init db

##### init virtual env because deploy process on dev machine
```bash
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$ python3 -m venv .venv
sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$ source ./.venv/bin/activate
(.venv) sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$
```
##### install dependancies
```bash
(.venv) sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$ pip install -r project/requirements.txt
Collecting fastapi==0.128.0 (from -r project/requirements.txt (line 2))
  Using cached fastapi-0.128.0-py3-none-any.whl.metadata (30 kB)
Collecting Jinja2==3.1.2 (from -r project/requirements.txt (line 3))
...
(.venv) sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$
```

##### run init db script
```bash
(.venv) sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task$ cd project/
(.venv) sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task/project$ python3 init_db.py
---------------------postgresql+psycopg2://sibir:sibirpass@localhost:5430/selery_app-------------------
2026-01-24 14:10:03,504 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2026-01-24 14:10:03,505 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-01-24 14:10:03,507 INFO sqlalchemy.engine.Engine select current_schema()
2026-01-24 14:10:03,507 INFO sqlalchemy.engine.Engine [raw sql] {}
...
```
#### check db initiation
##### connect to postgres
```bash
# connection props in compose_db.yml
(.venv) sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task/project$ psql -h localhost -p 5430 -d selery_app -U sibir
Password for user sibir: # sibirpass 
psql (16.11 (Ubuntu 16.11-0ubuntu0.24.04.1), server 18.1 (Debian 18.1-1.pgdg13+2))
WARNING: psql major version 16, server major version 18.
         Some psql features might not work.
Type "help" for help.

selery_app=# \dt
          List of relations
 Schema |    Name    | Type  | Owner
--------+------------+-------+-------
 public | index      | table | sibir
 public | indexprice | table | sibir
 public | stock      | table | sibir
 public | ticker     | table | sibir
(4 rows)

selery_app=# \q
(.venv) sibir007@sibir007:~/repos/deploy/db/simple_solutions_test_task/project$
```
##### connect to adminer http://localhost:8090/
![login](readme/admiter_login.png)
![adminer](readme/adminer.png)

### APP HOST
#### clone git repos
```bash
sibir007@sibir007:~/repos/deploy/app$ git clone https://github.com/sibir007/simple_solutions_test_task.git
Cloning into 'simple_solutions_test_task'...
remote: Enumerating objects: 292, done.
remote: Counting objects: 100% (292/292), done.
remote: Compressing objects: 100% (204/204), done.
remote: Total 292 (delta 169), reused 204 (delta 84), pack-reused 0 (from 0)
Receiving objects: 100% (292/292), 265.01 KiB | 1005.00 KiB/s, done.
Resolving deltas: 100% (169/169), done.
sibir007@sibir007:~/repos/deploy/app$ cd simple_solutions_test_task/
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$ ls
compose_app.yml  expample_env  project  README_dev.md
compose_db.yml   LICENSE       readme   README.md
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$
```
#### create .env file
```bash
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$ mv expample_env .env
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$
```
#### create logs files
```bash
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$ mkdir project/logs
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$ touch project/logs/celery.log
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$ touch project/logs/beat.log
```

#### run servises
```bash
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$ sudo docker compose -f compose_app.yml up -d
WARN[0000] No services to build
WARN[0000] Found orphan containers ([simple_solutions_test_task-adminer-1 postgres_db postgres_container]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
[+] up 5/5
 ✔ Container redis                                  Created                 0.2s
 ✔ Container worker                                 Created                 0.1s
 ✔ Container web                                    Created                 0.1s
 ✔ Container beat                                   Created                 0.1s
 ✔ Container simple_solutions_test_task-dashboard-1 Created                 0.1s
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$
```
#### checks
##### running tests
```bash
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$ sudo docker compose -f compose_app.yml exec web python -m pytest
============================== test session starts ==============================
platform linux -- Python 3.11.2, pytest-9.0.2, pluggy-1.6.0
rootdir: /usr/src/app
plugins: anyio-4.12.1
collected 7 items

tests/test_tasks.py .......                                               [100%]

=============================== 7 passed in 0.62s ===============================
sibir007@sibir007:~/repos/deploy/app/simple_solutions_test_task$
```

##### connect to flower  http://localhost:5555/

![flower](readme/flower.png)

##### test api from http://localhost:8000/docs

![fastapi1](readme/fast1.png)
![fastapi1](readme/fast2.png)

