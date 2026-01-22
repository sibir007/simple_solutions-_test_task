from datetime import datetime
from enum import Enum
from typing import Annotated, Literal
from fastapi import Body, FastAPI, Form, Path, Query, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from selery_app.tasks import create_task
from celery.result import AsyncResult
from shemas.fastapi_app_shemas import ResponseInem
from database.read_data import get_trick_index_info


app = FastAPI()
app.mount("/static", StaticFiles(directory="fastapi_app/static"), name="static")
test_templates = Jinja2Templates(directory="fastapi_app/templates")



@app.get("/{stock}")
async def home(
    stock: Annotated[Literal["deribit", "somestock"], Path(title="Stock", description="Stock for request")],
    ticker: Annotated[
        Literal["btc", "eth"], Query(title="Ticker", description="Ticker for request")
    ],
    index: Annotated[
        Literal["usd", "eurr"] | None, Query(title="Index", description="Index for request")
    ] = None,
    dates: Annotated[
        list[datetime] | None, Query(title="Dates", description="Dates for request", max_length=2)
    ] = None
) -> list[ResponseInem]:
    
    query_items = get_trick_index_info(stock, ticker, index, dates)
    
    return query_items


# @app.get("/test")
# async def test(request: Request):
#     return test_templates.TemplateResponse(
#         "test/home.html", context={"request": request}
#     )


# @app.get("/currency")
# async def test(request: Request):
#     return test_templates.TemplateResponse(
#         "currency/home.html", context={"request": request}
#     )


# @app.post("/tasks", status_code=201)
# def run_task(payload=Body(...)):
#     task_type = payload["type"]
#     task = create_task.delay(int(task_type))
#     return JSONResponse({"task_id": task.id})


# @app.get("/tasks/{task_id}")
# def get_status(task_id):
#     task_result = AsyncResult(task_id)
#     result = {
#         "task_id": task_id,
#         "task_status": task_result.status,
#         "task_result": task_result.result,
#     }
#     return JSONResponse(result)
