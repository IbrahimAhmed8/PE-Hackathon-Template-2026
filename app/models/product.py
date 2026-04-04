from peewee import CharField, DecimalField, IntegerField, Check
from app.database import BaseModel

class Product(BaseModel):
    name = CharField(unique=True)
    category = CharField()
    price = DecimalField(decimal_places=2, constraints=[Check('price >= 0')])
    stock = IntegerField(constraints=[Check('stock >= 0')])
