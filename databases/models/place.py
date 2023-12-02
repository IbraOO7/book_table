from unicodedata import category
from sqlalchemy import Column, ForeignKey, Integer, Text, String, Boolean, DECIMAL, DateTime
from sqlalchemy.orm import relationship
import datetime
from slugify import slugify
from databases.db_config import Base
from sqlalchemy_utils import URLType

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    slug = Column(String(100), unique=True)
    
    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super(Category, self).__init__(*args, **kwargs)
    
    place_category = relationship("Place", back_populates="category_related")

class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(Text)
    location = Column(String(200))
    longtitude = Column(String(200))
    latitude = Column(String(200))
    picture = Column(URLType)
    price = Column(DECIMAL(scale=2))
    available = Column(Boolean, default=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, default=datetime.datetime.now)
    slug = Column(String(100), unique=True)
    rating = Column(DECIMAL(scale=2))
    table_place_qty = Column(Integer)
    
    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super(Place, self).__init__(*args, **kwargs)
    
    category_id = Column(Integer, ForeignKey("category.id"))
    category_related = relationship("Category", back_populates="place_category")
    place_order = relationship("Cost", back_populates="place_related")

    