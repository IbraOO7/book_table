from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from databases.db_config import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    phone = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    level = Column(String(150), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    update_at = Column(DateTime, onupdate=datetime.now())
    user_related = relationship("Friends", back_populates="friend_related")

class Friends(Base):
    __tablename__ = 'friends'
    id = Column(Integer, primary_key=True)
    is_friend = Column(Boolean, default=False)
    accepted_at = Column(DateTime, nullable=False, default=datetime.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    friend_related = relationship("User", back_populates="user_related")
        
    
    