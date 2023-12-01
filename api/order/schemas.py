from pydantic import BaseModel, Json, ValidationError
from typing import Any, List, Dict
from datetime import datetime

class OrderModel(BaseModel):
    first_name : str
    last_name : str
    email: str
    address: str
    city: str
    created_date: datetime
    is_paid: bool
    payment_method: str
    payment_status: str
    is_paid: bool
    discount: int

class CreateOrder(BaseModel):
    first_name : str
    last_name : str
    email: str
    address: str
    city: str
    created_date: datetime
    is_paid: bool = False
    payment_method: str
    is_paid: bool