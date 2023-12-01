from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from databases.db_config import init_db
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from api.coupon.router import router as coupon_router
from api.order.router import router as order_router
from api.place.router import router as place_router
from api.login.router import router as login_router
from api.order_list.router import router as order_list_router
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
import os

middleware = [
    Middleware(SessionMiddleware, secret_key='450lfgf')
]
app = FastAPI(middleware=middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.on_event("startup")
async def on_startup():
    from databases.models.user import User, Friends
    from databases.models.place import Place, Category
    from databases.models.order import Order, Cost
    from databases.models.coupon import Coupon
    await init_db()

app.include_router(coupon_router)
app.include_router(order_router)
app.include_router(place_router)
app.include_router(login_router)
app.include_router(order_list_router)
    

