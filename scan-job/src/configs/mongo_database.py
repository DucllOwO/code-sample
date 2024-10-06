from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from configs import DATABASE_URL
from src.models.postgres_model import Transaction, ProjectModel, BlockTracking, Contract

# Connect to MongoDB
client = AsyncIOMotorClient(DATABASE_URL)
db = client['waterpump']


async def init_db_mongo():
    await init_beanie(database=db, document_models=[Transaction, ProjectModel, BlockTracking, Contract])
