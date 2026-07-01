import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aio_pika.abc import AbstractIncomingMessage
from rabbitmq import RabbitMQ

rabbitmq = RabbitMQ("amqp://guest:guest@localhost:5672/")


async def handle_order_created(message:AbstractIncomingMessage):
    try:
        data = json.loads(message.body.decode("utf-8"))
        print(f"Recieved order created: {data}")
        await message.ack()
    except Exception as e:
        await message.nack()
        print(f"Failed to parse message: {e}")


async def main():
    connection = await rabbitmq.connect()
    channel = await connection.channel()
    orders_exchange = await rabbitmq.declare_post_excange(channel)
    queue = await rabbitmq.declare_post_queue(channel=channel,exchange=orders_exchange)

    await queue.consume(handle_order_created)

    await asyncio.Future()

    await connection.close()

if __name__ == "__main__":
    asyncio.run(main())

    