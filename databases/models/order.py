from sqlalchemy import DECIMAL, Column, BigInteger, ForeignKey, String, DateTime, Integer, Text, Boolean
from databases.db_config import Base
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import EmailType
import datetime

class Order(Base):
    __tablename__ = 'orders'
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(EmailType)
    address = Column(Text)
    city = Column(String(150))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    payment_method = Column(String(100), nullable=False)
    payment_status = Column(String(50), nullable=False, default='Pending') 
    is_paid = Column(Boolean, default=False)
    order_place = relationship("Cost", back_populates="order_related")
    coupon_id = Column(Integer, ForeignKey('coupon.id'))
    coupon_related = relationship("Coupon", back_populates="order_coupon")
    discount = Column(Integer)
    
    def get_total_cost(self):
        total_cost = sum(place.get_cost() for place in self.places.all())
        return total_cost
    
class Cost(Base):
    __tablename__ = 'cost'
    id = Column(Integer, primary_key=True)
    price = Column(DECIMAL(scale=2))
    quantity = Column(Integer, default=1)
    place_id = Column(Integer, ForeignKey("place.id"))
    place_related = relationship("Place", back_populates="place_order")
    order_id = Column(BigInteger, ForeignKey("orders.id"))
    order_related = relationship("Order", back_populates="order_place")
    
    def get_cost(self):
        return self.price * self.quantity