from fastapi import APIRouter, Depends, Request
from fastapi.responses import UJSONResponse
from databases.db_config import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from databases.models.place import Place
from .schemas import PlaceModel, CreatePlace, CreateCategory
from .crud import *
import datetime
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/place",
    tags=["API Place"]
)

CRUDPlace = CRUDBase[Place, PlaceModel, CreatePlace]
crud_place = CRUDBase(Place)

@router.get('/data-place')
async def data_place(offset: int = 0, limit: int = None ,session: AsyncSession = Depends(get_session)):
    return await crud_place.multi_get(session, offset=offset, limit=limit)

@router.post('/create-place')
async def create_place(place: CreatePlace, request: Request, db: AsyncSession = Depends(get_session)):
    try:
        obj_in = place.dict()
        return await crud_place.create(db, obj_in)
    except Exception as e:
        print(e)
    return {"Ok"}

@router.get('/data-category')
async def data_category(offset: int = 0, limit: int = None ,session: AsyncSession = Depends(get_session)):
    return await crud_place.multi_get_category(session, offset=offset, limit=limit)

@router.post('/create-category')
async def create_category(place: CreateCategory, request: Request, db: AsyncSession = Depends(get_session)):
    try:
        obj_in = place.dict()
        return await crud_place.create_category(db, obj_in)
    except Exception as e:
        print(e)
    return {"Ok"}

    
