import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue, AbstractExchange
import json
from fastapi import Request

class RabbitMQAuthProducer:
    def __init__(self, rabbit_url: str):
        self.rabbit_url = rabbit_url
        self.connection: AbstractConnection = None
        self.channel: AbstractChannel = None
        self.exchange: AbstractExchange = None


        self.RSS_AUTH_EXCHANGE = "rss.auth.exchange"      
        self.RSS_AUTH_ROUTING_KEY = "rss.auth.routing.key"

    async def connect(self):
        self.connection = await aio_pika.connect(self.rabbit_url)
        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(
            self.RSS_AUTH_EXCHANGE,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True
        )

    async def publish(self, message_data: dict, routing_key:str):
        if not self.exchange:
            await self.connect()
        message_body = json.dumps(message_data).encode("utf-8")
        
        await self.exchange.publish(
            aio_pika.Message(
                body=message_body,
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=routing_key
        )
    
    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

def get_rabbit_auth_producer(request: Request) -> RabbitMQAuthProducer:
    return request.app.state.rabbitmq_auth_producer