from aio_pika import message
import aio_pika
import aio_pika
from aio_pika.abc import AbstractChannel,AbstractConnection, AbstractQueue, AbstractExchange
from app.core.config import settings
import json



class RabbitMQ:
    def __init__(self, rabbit_url:str):
        self.connection : AbstractConnection = None
        self.rabbit_url = rabbit_url
        self.URL_GENERATOR_EXCHANGE = "rss.exchange"
        self.URL_GENERATOR_QUEUE = "rss.tasks.queue"
        self.URL_GENERATOR_ROUTING_KEY = "rss.task.convert"
    
    async def connect(self) -> AbstractConnection:
        self.connection = await aio_pika.connect_robust(self.rabbit_url)
        return self.connection

    async def declare_url_generator_exchange(self, channel:AbstractChannel) -> AbstractExchange:
        return await channel.declare_exchange(
            self.URL_GENERATOR_EXCHANGE,
            type = aio_pika.ExchangeType.TOPIC
        )

    async def declare_url_generator_queue(
        self, 
        channel:AbstractChannel,
        exchange: AbstractExchange,
    ) -> AbstractQueue:
        queue = await channel.declare_queue(self.URL_GENERATOR_QUEUE, durable=True)
        await queue.bind(exchange, routing_key=self.URL_GENERATOR_ROUTING_KEY)
        return queue

    async def publish_json(self, exchange: AbstractExchange, routing_key: str, data: dict):
        message = aio_pika.Message(
            body=json.dumps(data).encode(),
            content_type="application/json"
        )
        await exchange.publish(message, routing_key=routing_key)
    
    async def close(self):
        if self.connection:
            await self.connection.close()

