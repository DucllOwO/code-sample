from src.config import settings
from src.database import metadata, dynamic_engine, database


async def on_start():
    await database.connect()
    metadata.create_all(dynamic_engine)


async def on_shutdown():
    await database.disconnect()
