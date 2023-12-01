from pydantic import BaseModel, Json, ValidationError
from typing import Any, List, Dict
from datetime import datetime

class CouponModel(BaseModel):
    code: str
    discount: int
    active: bool

class CreateCoupon(BaseModel):
    code: str
    valid_from: datetime
    valid_to: datetime
    discount: int
    active: bool
