from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from databases.models.user import User
from databases.db_config import get_session
from .schemas import CreateUser, Users
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import CRUDBase
from service.hashing import Hashing
from service.security import authenticate_user, get_current_user, create_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/user',
    tags=["User API"]
)

CRUDUser = CRUDBase[User, Users, CreateUser]
crud_user = CRUDBase(User)

@router.get('/')
async def users(offset: int = 0, limit: int = None, session: AsyncSession = Depends(get_session)):
    return await crud_user.multi_get(session, offset=offset, limit=limit)

@router.post('/register')
async def register(data: CreateUser, session: AsyncSession = Depends(get_session)):
    db_usr = await session.execute(select(User).filter(User.phone == data.phone))
    db_user = db_usr.scalars().first()
    if db_user:
        raise HTTPException(status_code=400,detail="User telah terdapat")
    data = await crud_user.create_data_user(session, data)
    return await create_token(data)

@router.put("/edit-user/{id}")
async def edit_users(user: CreateUser, id: int = None, session: AsyncSession = Depends(get_session)):
    db_usr = await session.execute(select(User).filter(User.id == id))
    db_user = db_usr.scalars().first()
    if db_user:
        raise HTTPException(status_code=400,detail="User telah terdapat")
    data = await crud_user.update_data_user(session, data)
    return await create_token(data)

@router.post('/api/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return await create_token(user)

@router.get('/api/users/me', response_model=Users)
async def get_user(user: Users = Depends(get_current_user)):
    return user