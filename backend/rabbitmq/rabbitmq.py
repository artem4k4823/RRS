from aio_pika import message
import aio_pika
import aio_pika
from aio_pika.abc import AbstractChannel,AbstractConnection, AbstractQueue, AbstractExchange
from app.core.config import settings
import json




pending_requests = {}

class RabbitMQ:
    def __init__(self, rabbit_url:str):
        self.connection : AbstractConnection = None
        self.rabbit_url = rabbit_url
        self.URL_GENERATOR_EXCHANGE = "rss.exchange"
        self.URL_GENERATOR_QUEUE = "rss.tasks.queue"
        self.RESULT_QUEUE = "rss.result.queue"
        self.URL_GENERATOR_ROUTING_KEY = "rss.task.convert"
        self.RESULT_ROUTING_KEY = "rss.result"
        
    
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


    async def declare_result_queue(
        self,
        channel: AbstractChannel,
        exchange: AbstractExchange,
    ) -> AbstractQueue:
        queue = await channel.declare_queue(self.RESULT_QUEUE, durable=True)
        await queue.bind(exchange, routing_key=self.RESULT_ROUTING_KEY)
        return queue

        
    async def publish_json(self, exchange: AbstractExchange, routing_key: str, data: dict):
        message = aio_pika.Message(
            body=json.dumps(data).encode(),
            content_type="application/json"
        )
        await exchange.publish(message, routing_key=routing_key)


    async def start_listening(self, channel: AbstractChannel, exchange: AbstractExchange, callback_func):
        queue = await self.declare_result_queue(channel, exchange)
        await queue.consume(callback_func)

    async def process_result_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            body = message.body.decode()
            data = json.loads(body)
            task_id = data.get('id')
            xml_content = data.get('xml')
            print(f"[x] Backend received result for URL: {data.get('url')} (id: {task_id})")
            
            if task_id in pending_requests:
                future = pending_requests[task_id]
                if not future.done():
                    future.set_result(xml_content)
            else:
                print(f"[!] No pending request found for id {task_id}")
    
    async def close(self):
        if self.connection:
            await self.connection.close()

