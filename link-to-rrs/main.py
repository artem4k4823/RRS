from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
import asyncio
from app.rabbitmq.rabbitmq import RabbitMQConsumer, process_message
from app.core.config import settings
from app.api_v1.get_rrs import router as rrs_router


rabbitmq = RabbitMQConsumer(settings.RABBIT_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = await rabbitmq.connect()
    asyncio.create_task(rabbitmq.start_listening(process_message))
    yield



app = FastAPI(title="Link to RRS Service", lifespan=lifespan)
app.include_router(rrs_router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "link-to-rrs"}

if __name__ == "__main__":
   
    uvicorn.run("main:app", host="127.0.0.1", port=8083, reload=True)