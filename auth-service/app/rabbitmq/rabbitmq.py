import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue, AbstractExchange


class RabbitMQ:
    def __init__(self, rabbit_url: str):
        self.rabbit_url = rabbit_url
        self.connection: AbstractConnection = None
        self.channel: AbstractChannel = None
        self.queue: AbstractQueue | None = None
        self.RSS_AUTH_EXCHANGE = "rss.auth.exchange"
        self.RSS_AUTH_QUEUE = "rss.auth.queue"
        self.RSS_AUTH_ROUTING_KEY = "rss.auth.routing.key"

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbit_url)
        self.channel = await self.connection.channel()

        exchange = await self.channel.declare_exchange(
            self.RSS_AUTH_EXCHANGE, 
            type=aio_pika.ExchangeType.TOPIC
        )
       
        queue: AbstractQueue = await self.channel.declare_queue(
            self.RSS_AUTH_QUEUE, 
            durable=True 
        )

        await queue.bind(exchange, routing_key=self.RSS_AUTH_ROUTING_KEY)

    async def start_listening(self, callback_func):
        queue = await self.connect()
        if not self.queue:
            await self.connect()
        await self.queue.consume(callback_func)

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()