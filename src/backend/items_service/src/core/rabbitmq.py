import aio_pika
from src.core.config import cfg


async def send_message_item(message: str):
    connection = await aio_pika.connect_robust(cfg.rabbit_connection)
    channel = await connection.channel()
    queue = await channel.declare_queue('create_item_queue', durable=True)

    await channel.default_exchange.publish(
        aio_pika.Message(body=message.encode(),
                         delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
        routing_key='create_item_queue'
    )
    
    await connection.close()


async def send_message_category(message: str):
    connection = await aio_pika.connect_robust(cfg.rabbit_connection)
    channel = await connection.channel()
    queue = await channel.declare_queue('create_category_queue', durable=True)

    await channel.default_exchange.publish(
        aio_pika.Message(body=message.encode(),
                         delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
        routing_key='create_category_queue'
    )
    
    await connection.close()
