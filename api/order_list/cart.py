from databases.models.coupon import Coupon
from databases.models.place import Place, Category
from fastapi.encoders import jsonable_encoder

secret_key = 'cart'

class Cart(object):
    def __init__(self, request, db):
        self.session = request.session
        self.db = db
        cart = self.session.get(secret_key)
        
        if not cart:
            cart = self.session[secret_key] = {}
        
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')
    
    async def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id][quantity] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    async def get_total_price(self):
        return sum(float(item['price']) * float(item['quantity']) for item in self.cart.values())
    
    @property
    async def coupon(self):
        if self.coupon_id:
            kupon = await session.execute(select(Coupon).filter(Coupon.id == self.coupon_id))
            return kupon.scalars().first()
        return None
    
    async def get_discount(self):
        if self.coupon:
            return float("{:.2f}".format((self.coupon.discount / float(100)) * self.get_total_price()))
        return float("{:.2f}".format(0))
    
    async def get_total_price_after_discount(self):
        return float("{:.2f}".format(self.get_total_price() - self.get_discount()))
            
            
        