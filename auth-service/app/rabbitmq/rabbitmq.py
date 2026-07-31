import aio_pika
import json
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue, AbstractExchange, AbstractMessage
from app.auth.jwt_operations import create_access_token, create_refresh_token


class RabbitMQ:
    def __init__(self, rabbit_url: str):
        self.rabbit_url = rabbit_url
        self.connection: AbstractConnection = None
        self.channel: AbstractChannel = None
        self.queue: AbstractQueue | None = None
        self.RSS_AUTH_EXCHANGE = "rss.auth.exchange"
        self.RSS_AUTH_QUEUE = "rss.auth.queue"
        self.RSS_AUTH_ROUTING_KEY = "rss.auth.routing.key"
        self.RSS_AUTH_RESPONSE_ROUTING_KEY = "rss.auth.response.key"

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbit_url)
        self.channel = await self.connection.channel()

        exchange = await self.channel.declare_exchange(
            self.RSS_AUTH_EXCHANGE, 
            type=aio_pika.ExchangeType.TOPIC,
            durable=True
        )
       
        self.queue = await self.channel.declare_queue(
            self.RSS_AUTH_QUEUE, 
            durable=True 
        )

        await self.queue.bind(exchange, routing_key=self.RSS_AUTH_ROUTING_KEY)

    async def start_listening(self, callback_func):
        if not self.queue:
            await self.connect()
        await self.queue.consume(callback_func)

    async def process_message(self, message: AbstractMessage):
        async with message.process():
            body = message.body.decode()
            data = json.loads(body)
            print(f"[auth-service] Received request: {data}")
            
            task_id = data.get("id")
            token_type = data.get("TOKEN_TYPE", "access")
            user_id = data.get("sub") or data.get("user_id")

            if token_type == "refresh":
                token = create_refresh_token(user_id)
            else:
                token = create_access_token(user_id)

            reply_routing_key = message.reply_to or self.RSS_AUTH_RESPONSE_ROUTING_KEY
            exchange = await self.channel.get_exchange(self.RSS_AUTH_EXCHANGE)
            
            response_payload = {
                "id": task_id,
                "token": token,
                "status": "success"
            }
            
            response_msg = aio_pika.Message(
                body=json.dumps(response_payload).encode("utf-8"),
                content_type="application/json",
                correlation_id=message.correlation_id
            )
            await exchange.publish(response_msg, routing_key=reply_routing_key)
            print(f"[auth-service] Sent response token for task {task_id}")

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()