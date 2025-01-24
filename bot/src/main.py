from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import os

from dotenv import load_dotenv

PYTHON_ENV = os.getenv("PYTHON_ENV")

env_file = (
    "/usr/src/app/.dev.env" if PYTHON_ENV == "development" else "/usr/src/app/.env"
)

load_dotenv(env_file)

from src.expenses.infrastructure.entry_point.http.expense_routes import (
    router as expenses_router,
)
from src.expenses.infrastructure.entry_point.events.expenses_subscriber import (
    inboundMessageProcessor,
)
from src.shared.postgres.connection import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    inboundMessageProcessorTask = asyncio.create_task(inboundMessageProcessor().run())
    yield
    inboundMessageProcessorTask.cancel()
    await close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(expenses_router)
