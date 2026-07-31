import asyncio
import uuid
import json
import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue, AbstractExchange, AbstractIncomingMessage
from fastapi import Request

pending_auth_requests = {}


class RabbitMQAuthProducer:
    def __init__(self, rabbit_url: str):
        self.rabbit_url = rabbit_url
        self.connection: AbstractConnection = None
        self.channel: AbstractChannel = None
        self.exchange: AbstractExchange = None
        self.response_queue: AbstractQueue = None

        self.RSS_AUTH_EXCHANGE = "rss.auth.exchange"      
        self.RSS_AUTH_ROUTING_KEY = "rss.auth.routing.key"
        self.RSS_AUTH_RESPONSE_QUEUE = "rss.auth.response.queue"
        self.RSS_AUTH_RESPONSE_ROUTING_KEY = "rss.auth.response.key"

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbit_url)
        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(
            self.RSS_AUTH_EXCHANGE,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        self.response_queue = await self.channel.declare_queue(
            self.RSS_AUTH_RESPONSE_QUEUE,
            durable=True
        )
        await self.response_queue.bind(self.exchange, routing_key=self.RSS_AUTH_RESPONSE_ROUTING_KEY)
        await self.response_queue.consume(self.process_response_message)

    async def process_response_message(self, message: AbstractIncomingMessage):
        async with message.process():
            body = message.body.decode()
            data = json.loads(body)
            task_id = data.get("id")
            token = data.get("token")
            print(f"[backend auth producer] Received token response for task_id {task_id}")

            if task_id in pending_auth_requests:
                future = pending_auth_requests.pop(task_id)
                if not future.done():
                    future.set_result(token)

    async def request_token(self, token_type: str, data: dict) -> str:
        if not self.exchange:
            await self.connect()

        task_id = str(uuid.uuid4())
        message_data = data.copy()
        message_data["id"] = task_id
        message_data["TOKEN_TYPE"] = token_type

        loop = asyncio.get_running_loop()
        future = loop.create_future()
        pending_auth_requests[task_id] = future

        message_body = json.dumps(message_data).encode("utf-8")
        await self.exchange.publish(
            aio_pika.Message(
                body=message_body,
                content_type="application/json",
                reply_to=self.RSS_AUTH_RESPONSE_ROUTING_KEY,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=self.RSS_AUTH_ROUTING_KEY
        )

        try:
            token = await asyncio.wait_for(future, timeout=10.0)
            return token
        except asyncio.TimeoutError:
            pending_auth_requests.pop(task_id, None)
            raise RuntimeError("Timeout waiting for token from auth-service")

    async def publish(self, message_data: dict, routing_key: str):
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