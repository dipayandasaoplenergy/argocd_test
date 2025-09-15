from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models
from .db import engine, Base, get_db
import logging, json
from fastapi import FastAPI

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("app.log", mode="a")
file_handler.setFormatter(JsonFormatter())
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(JsonFormatter())
logger.addHandler(stream_handler)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # create tables for demo (prod → Alembic migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health():
    logger.info("Health check requested")
    return {"status": "ok"}


@app.post("/users/")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    user = models.User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@app.get("/users/")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    return result.scalars().all()
