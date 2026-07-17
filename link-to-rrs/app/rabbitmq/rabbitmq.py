import json
import asyncio
import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue, AbstractExchange

class RabbitMQConsumer:
    def __init__(self, rabbit_url: str):
        self.rabbit_url = rabbit_url
        self.connection: AbstractConnection = None
        self.channel: AbstractChannel = None
        
        self.RSS_EXCHANGE = "rss.exchange"
        self.RSS_QUEUE = "rss.tasks.queue"
        self.RSS_ROUTING_KEY = "rss.task.convert"

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbit_url)
        self.channel = await self.connection.channel()
        
       
        exchange = await self.channel.declare_exchange(
            self.RSS_EXCHANGE, 
            type=aio_pika.ExchangeType.TOPIC
        )
       
        queue: AbstractQueue = await self.channel.declare_queue(
            self.RSS_QUEUE, 
            durable=True 
        )
        
        await queue.bind(exchange, routing_key=self.RSS_ROUTING_KEY)
        return queue

    async def start_listening(self, callback_func):
        queue = await self.connect()
     
        await queue.consume(callback_func)
        print("[*] Waiting for messages. To exit press CTRL+C")
   
        await asyncio.Future() 
    
    async def publish_json(self, exchange_name: str, routing_key: str, data: dict):
        if not self.channel:
            await self.connect()
        exchange = await self.channel.get_exchange(exchange_name)
        message = aio_pika.Message(
            body=json.dumps(data).encode(),
            content_type="application/json"
        )
        await exchange.publish(message, routing_key=routing_key)

    async def close(self):
        if self.connection:
            await self.connection.close()

async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
     
        
        body = message.body.decode()
        data = json.loads(body)
        
        print(f"[x] Получено сообщение: {data}")
        print(f"ID: {data.get('id')}")
        print(f"Событие: {data.get('event')}")
        print(f"Заголовок: {data.get('title')}")
        
        
        url = data.get('url') or data.get('link')
        if url:
            print(f"[*] Получен URL из очереди: {url}")
           
        else:
            print("[!] В сообщении не найден URL")

