import aiohttp
import asyncio
from fastapi import APIRouter, Depends, Request
from fastapi.responses import UJSONResponse
from databases.db_config import get_session
import json
from sqlalchemy.ext.asyncio import AsyncSession
from databases.models.coupon import Coupon
from fastapi.responses import RedirectResponse
from .schemas import CouponModel, CreateCoupon
from .crud import *
import datetime
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix='/coupon',
    tags=['Coupons']
)

CRUDCoupon = CRUDBase[Coupon, CouponModel, CreateCoupon]
crud_coupon = CRUDBase(Coupon)

@router.post('/create-kupon')
async def create_coupon(coupon: CreateCoupon, request: Request, db: AsyncSession = Depends(get_session)):
    try:
        obj_in = coupon.dict()
        return await crud_coupon.create(db, obj_in)
    except Exception as e:
        print(e)
    return {"Ok"}

@router.post('/apply-kupon')
async def coupon_apply(code: str, request: Request, db: AsyncSession = Depends(get_session)):
    now = datetime.datetime.now()
    try:
        coupon = await db.execute(select(Coupon).filter(Coupon.code == code,
                                         Coupon.valid_from.__le__(now),
                                         Coupon.valid_to.__ge__(now),
                                         Coupon.active == True))
        kupon = coupon.scalars().first()
        request.session['coupon_id'] = kupon.id # Mengkuti session pada frontend
        return jsonable_encoder("Kupon Valid")
    except:
        request.session['coupon_id'] = None
        return jsonable_encoder("Kupon Tidak Valid")
    return {"Ok"}


    
