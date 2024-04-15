from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.prod_config import settings


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


app = get_application()
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import UUID4, BaseModel

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


@app.get("/items/")
    """
    This Python function defines an endpoint that reads items with an optional query parameter.

    Args:
      q (Annotated[list[str], Query()]): The parameter `q` in the `read_items` function is a query parameter that expects a
    list of strings. It has a default value of an empty list `[]`. This parameter is used to filter items based on the
    provided list of strings.

    Returns:
      The code defines a FastAPI endpoint at "/items/" that accepts a query parameter "q" as a list of strings. If no value
    is provided for "q", it defaults to an empty list. When the endpoint is accessed, it returns a dictionary containing
    the query parameter "q" with its value.
    """
async def read_items(q: Annotated[list[str], Query()] = []):
    query_items = {"q": q}
    return query_items
