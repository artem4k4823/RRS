import aio_pika
from aio_pika.abc import AbstractChannel,AbstractConnection, AbstractQueue, AbstractExchange
from app.core.config import settings
import json



class RabbitMQ:
    def __init__(self, rabbit_url:str):
        self.connection : AbstractConnection = None
        self.channel : AbstractChannel = None
        self.rabbit_url = rabbit_url
        self.POST_QUEUE = "posts.create"
        self.POST_EXHANGE = "posts"
        self.POST_ROUTING_KEY = "post.created"
    
    async def connect(self) -> AbstractConnection:
        return await aio_pika.connect_robust(self.rabbit_url)

    async def declare_post_excange(self, channel:AbstractChannel) -> AbstractChannel:
        return await channel.declare_exchange(self.POST_EXHANGE)

    async def declare_post_queue(
        self, 
        channel:AbstractChannel,
        exchange: AbstractExchange,
        ) -> AbstractQueue:
       queue: AbstractQueue = await channel.declare_queue(self.POST_QUEUE)
       await queue.bind(exchange, routing_key=self.POST_ROUTING_KEY)
       return queue

    async def publish_json(self, exchange: AbstractExchange, routing_key: str, data: dict):
        message = aio_pika.Message(json.dumps(data).encode())
        await exchange.publish(message, routing_key)


