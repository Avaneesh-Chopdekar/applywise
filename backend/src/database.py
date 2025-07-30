import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

load_dotenv()


async def init_db():
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    database = client.get_database("applywise")

    await init_beanie(database, document_models=[])

    return database
