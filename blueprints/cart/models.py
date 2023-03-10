import datetime as dt
from peewee import *
from app import db
from blueprints.auth.models import User
from blueprints.product.models import Product


class Cart(Model):
    user = ForeignKeyField(User, null=False, related_name='carts')
    active = BooleanField(null=False, default=True)
    created_at = DateTimeField(default=dt.datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db

    @classmethod
    def get_active_cart(cls, user_id):
        # cart = Cart.select().where(Cart.user_id == user_id, Cart.active == True)
        carts = Cart.filter(user_id=user_id, active=True)
        if not carts:
            cart = Cart.create(user_id=user_id)
        else:
            cart = carts[0]
        return cart

    def get_total_price(self):
        total_price = 0
        cart_items = CartItem.filter(cart=self)
        for item in cart_items:
            total_price += item.get_total_price()
        return total_price


class CartItem(Model):
    cart = ForeignKeyField(Cart, null=False)
    product = ForeignKeyField(Product, null=False)
    amount = IntegerField(null=False, default=1)
    created_at = DateTimeField(default=dt.datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db

    def get_total_price(self):
        return self.product.price * self.amount


class Order(Model):
    cart = ForeignKeyField(Cart, null=False, related_name='orders')
    total = IntegerField(null=False, default=0)
    address = CharField(null=False)
    created_at = DateTimeField(default=dt.datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db
