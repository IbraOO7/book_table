from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, BigInteger
from databases.db_config import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Coupon(Base):
    __tablename__ = 'coupon'
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    discount = Column(Integer)
    active = Column(Boolean)
    order_coupon = relationship("Order", back_populates="coupon_related")