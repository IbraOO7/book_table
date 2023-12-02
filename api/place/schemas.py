from pydantic import BaseModel, Json, ValidationError
from typing import Any, List, Dict
from datetime import datetime

class PlaceModel(BaseModel):
    name: str
    description: str
    location: str
    longtitude: str
    latitude: str
    picture: str
    price: float
    available: bool
    create_date: datetime
    update_date: datetime
    slug: str
    rating: float
    category_id: int

class CreatePlace(BaseModel):
    name: str
    description: str
    location: str
    longtitude: str
    latitude: str
    picture: str
    price: float
    available: bool
    create_date: datetime
    update_date: datetime
    slug: str
    rating: float
    table_place_qty: int
    category_id: int

class CategoryModel(BaseModel):
    name: str
    slug: str

class CreateCategory(BaseModel):
    name: str
    slug: str