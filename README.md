# simple_solutions-_test_task
https://testdriven.io/blog/fastapi-and-celery/
https://python.plainenglish.io/asynchronous-task-queuing-with-celery-d9709364e686

```sh
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ sudo docker compose up -d
WARN[0000] /home/sibir007/repos/simple_solutions-_test_task/compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion WARN[0000] No services to build                         
[+] up 3/3
 ✔ Volume simple_solutions-_test_task_pgdata     Created              0.0s 
 ✔ Container simple_solutions-_test_task-redis-1 Running              0.0s 
 ✔ Container postgres_db                         Created              0.1s 
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ sudo dosker ps
[sudo] password for sibir007: 
sudo: dosker: command not found
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ sudo docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS          PORTS                                         NAMES
41da061eaaa3   postgres:latest   "docker-entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:5430->5432/tcp, [::]:5430->5432/tcp   postgres_db
4d6415e4ab01   redis:latest      "docker-entrypoint.s…"   2 hours ago      Up 2 hours      6379/tcp                                      simple_solutions-_test_task-redis-1
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ psql -h localhost -p 5430 -d postgres -U postgres
Password for user postgres: 
postgres=# CREATE DATABASE celery;
CREATE DATABASE
postgres=# SELECT datname, dattablespace FROM pg_catalog.pg_database;
  datname  | dattablespace 
-----------+---------------
 postgres  |          1663
 celery    |          1663
 template1 |          1663
 template0 |          1663
(4 rows)
postgres=# \c celery
You are now connected to database "celery" as user "postgres".
celery=# \dt
Did not find any relations.
celery=# \q
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ 
```

```sh
sudo docker compose up -d --no-deps --build <service_name>
```

```sh
sudo docker compose exec web python -m pytest
```

```sh
(.venv) sibir007@sibir007:~/repos/simple_solutions_test_task$ redis-cli ping
PONG
```

```sh
sudo docker compose exec web python -m pytest -k "test_mock_task"
```