from fastapi import APIRouter, Depends, Form, status, Request, BackgroundTasks
from pydantic import EmailStr
from sqlalchemy.orm import Session
from api.order_list.cart import Cart
from databases.db_config import get_session
from .crud import *
from fastapi.responses import RedirectResponse
from .mail import Mail
from databases.models.order import Order, Cost
from databases.models.place import Place
from .schemas import OrderModel, CreateOrder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix='/order', tags=["Order API"])

CRUDOrder= CRUDBase[Order, OrderModel, CreateOrder]
crud_order = CRUDBase(Order)

secret_key = 'cart'

@router.get('/data-order/{id}')
async def data_order(id: int ,session: AsyncSession = Depends(get_session)):
    return await crud_order.get(session, id=id)

@router.post('/create_order')
async def order_add(order_id: int, orders: CreateOrder, background_tasks: BackgroundTasks, 
                    request: Request, coupon: str = None, db:AsyncSession=Depends(get_session)):
    cart = Cart(request, db)
    obj_in = orders.dict()
    db_order = await crud_order.create(db, obj_in)
    order_id = db_order.id
    request.session['order_id'] = order_id
    total_price = cart.get_total_price_after_discount()
    result = await db.execute(select(Place).filter(Place.id == 1))
    places = result.scalars().all()
    print(places)
    now = datetime.datetime.now()
    for item in places:
        data = {
            "price": item.price,
            "place_id": item.id,
            "order_id": order_id
        }
        await crud_order.create_order(db, data)
    mail = Mail()
    background_tasks.add_task(mail.send_notification) # Harus di sambungkan ke GMAIL API / Message Broker terlebih dahulu
    return jsonable_encoder("Processing Order")