import time
from .app import app
from celery import Celery
from celery.schedules import crontab
import requests

@app.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@app.task
def test(msg: str):
    print(msg)
    return True

@app.task
def get_coin_info(coin: str):
    pass

@app.task
def get_index_price(exchange: str, index_name: str):
    url = f"https://test.deribit.com/api/v2/public/get_index_price?index_name={index_name}"
    response = requests.get(url)
    print(response.text)

@app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )
    

# from celery.signals import task_received

# @task_received.connect()