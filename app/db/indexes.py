from app.db.mongodb import get_db
from app.db.collections import RESUME_COLLECTION

def create_indexes():
    db = get_db()
    db[RESUME_COLLECTION].create_index("created_at")
