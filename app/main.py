from typing import Annotated

from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import UUID4, BaseModel

# from src.config import settings


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


# app = get_application()


# Instantiate FastAPI app
app = FastAPI()


class Item(BaseModel):
    id: UUID4
    name: str
    description: str
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    item_as_dict = dict(item)
    print(item.price)
    if item.price:
        item_as_dict.update({"price_w_tax": item.price + item.tax})

    return item_as_dict


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
