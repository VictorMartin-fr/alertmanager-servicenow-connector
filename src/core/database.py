from pymongo import AsyncMongoClient
from src.core.config import settings

class Database:
    client: AsyncMongoClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    db_instance.client = AsyncMongoClient(f"mongodb://{settings.mongodb.username}:{settings.mongodb.password}@{settings.mongodb.hostname}:{settings.mongodb.port}")
    db_instance.db = db_instance.client[settings.mongodb.database]

def close_mongo_connection():
    db_instance.client.close()