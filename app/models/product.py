from peewee import CharField, DateTimeField, IntegerField, TextField, BooleanField
from app.database import BaseModel

class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    created_at = DateTimeField()

    class Meta:
        table_name = 'users'

class Url(BaseModel):
    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    short_code = CharField(unique=True)
    original_url = TextField()
    title = CharField(null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'urls'

class Event(BaseModel):
    id = IntegerField(primary_key=True)
    url_id = IntegerField()
    user_id = IntegerField()
    event_type = CharField()
    timestamp = DateTimeField()
    details = TextField(null=True)

    class Meta:
        table_name = 'events'