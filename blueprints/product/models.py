import datetime as dt
from peewee import *
from app import db


class Product(Model):
    name = CharField(null=False)
    price = FloatField(null=False, default=float(0))
    description = TextField(null=False)
    stock = IntegerField(null=False, default=0)
    hidden = BooleanField(null=False, default=False)
    created_at = DateTimeField(default=dt.datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db

    @property
    def is_available(self):
        if self.stock > 0 and not self.hidden:
            return True
        return False

    @classmethod
    def get_available_products(cls):
        products = Product.select().where(Product.stock > 0, Product.hidden == False)
        return products


class ProductImage(Model):
    image = CharField(null=False)
    product = ForeignKeyField(Product, null=False, related_name='images')

    class Meta:
        database = db
