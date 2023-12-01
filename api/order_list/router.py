from fastapi import APIRouter, Depends, status, Request, Form
from .cart import Cart
from databases.models.place import Place
from databases.models.order import Order
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from databases.db_config import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter(
    prefix='/order-list',
    tags=["Processing Order"]
)

@router.post('/add')
async def order_add(id:int, quantity:int, update:bool, request: Request, db: AsyncSession = Depends(get_session)):
    cart = Cart(request,db)
    result = await db.execute(select(Place).filter(Place.id == id))
    places = result.scalars().first()
    print(places)
    await cart.add(product=places,quantity=quantity,update_quantity=update)
    return jsonable_encoder("Success")

@router.post('/done')
async def checkout_payment(order_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Order).filter_by(id = order_id))
    order = result.scalars().first()
    order.is_paid = True
    order.payment_status = "Success"
    await db.commit()
    return jsonable_encoder("Your Order Has Been Created")


    