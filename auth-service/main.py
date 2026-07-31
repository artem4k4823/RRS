from app.rabbitmq.rabbitmq import RabbitMQ
import uvicorn
from contextlib import asynccontextmanager
from sys import prefix
from fastapi import FastAPI
from app.core.config import settings
import uvicorn


rabbitmq = RabbitMQ(settings.RABBIT_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq.start_listening(rabbitmq.process_message)
    yield
    await rabbitmq.close()
app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8084, reload=True)