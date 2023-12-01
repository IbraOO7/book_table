from typing import Any, List, Dict, Generic, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from databases.models.user import User
from datetime import datetime
from .schemas import Users
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from service.hashing import Hashing

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model
            
    async def create_data_user(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = dict(obj_in)
        obj_in_data["password"] = Hashing.bcrypt(obj_in_data["password"])
        db_obj = self._model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        return db_obj
    
    async def get(self, session: AsyncSession, *args, **kwargs) -> Optional[ModelType]:
        result = await session.execute(select(self._model).filter(*args).filter_by(**kwargs))
        return result.scalars().first()
    
    async def multi_get(self, session: AsyncSession, *args, offset: int = 0, limit: int = 100, **kwargs) -> List[ModelType]:
        result = await session.execute(select(self._model).filter(*args).filter_by(**kwargs).offset(offset).limit(limit))
        return result.scalars().all()
        
    async def update_data_user(self, session: AsyncSession, *args, 
                     obj_in: Union[UpdateSchemaType, Dict[str, Any]], db_obj: Optional[ModelType] = None, 
                     **kwargs) -> Optional[ModelType]:
        db_obj = db_obj or await self.get(session, **kwargs)
        if db_obj is not None:
            obj_data = db_obj.dict()
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
                session.add(db_obj)
                await session.commit()
            return db_obj
    
    async def delete_data_user(self, session: AsyncSession, *args, db_obj: Optional[ModelType] = None,**kwargs) -> ModelType:
        db_obj = db_obj or await self.get(session, *args, **kwargs)
        await session.delete(db_obj)
        await session.commit()
        return db_obj
    
