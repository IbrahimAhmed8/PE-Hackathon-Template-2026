from app import create_app
from app.database import db
from app.models.product import Product

app = create_app()
with app.app_context():
    print("[*] Initializing Database Tables...")
    db.create_tables([Product], safe=True)
    print("[+] Database Initialized Successfully!")
