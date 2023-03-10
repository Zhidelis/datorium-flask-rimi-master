import datetime as dt
from peewee import *
from app import db


class User(Model):
    name = CharField(null=False)
    email = CharField(null=False, unique=True)
    password = CharField(null=False)
    is_admin = BooleanField(null=False, default=False)
    created_at = DateTimeField(default=dt.datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db
