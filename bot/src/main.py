from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

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
