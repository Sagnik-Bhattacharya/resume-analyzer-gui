from app.db.mongodb import get_db
from app.db.collections import RESUME_COLLECTION

class ResumeRepository:
    def __init__(self):
        self.collection = get_db()[RESUME_COLLECTION]

    def save(self, data: dict):
        self.collection.insert_one(data)

    def fetch_all(self):
        return list(self.collection.find().sort("created_at", -1))
