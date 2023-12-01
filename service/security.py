import jwt
import fastapi.security as security
import datetime
from sqlalchemy import select
from databases.models.user import User
from fastapi import Depends, FastAPI, HTTPException
from databases.db_config import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from api.login.schemas import CreateUser, Users
from .hashing import Hashing

JWT_SECRET = 'mYs3cr3t$'
oauth2schema = security.OAuth2PasswordBearer(tokenUrl='/user/api/token')

async def authenticate_user(username: str, password: str, db: AsyncSession):
    usr = await db.execute(select(User).filter_by(username=username))
    user = usr.scalars().first()
    if not user:
        return False 
    if not Hashing.verify(user.password,password):
        return False
    return user

async def create_token(user: User):
    user_obj = Users.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")

async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = await db.get(User,payload["id"])
    except:
        raise HTTPException(status_code=401, detail="Invalid Username or Password")
    return Users.from_orm(user)


    