from typing import Annotated

from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import UUID4, BaseModel


class Item(BaseModel):
    id: UUID4
    name: str
    description: str
    price: float
    tax: float | None = None
