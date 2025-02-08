import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

# ✅ Updated QuestDB Connection URL
DATABASE_URL = "postgresql+asyncpg://admin:@localhost:8812/qdb"

async def test_connection():
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")  # Simple test query
            print("✅ Connected to QuestDB successfully!")
            print("Result:", result.fetchall())
    except Exception as e:
        print("❌ Connection failed:", str(e))

asyncio.run(test_connection())
