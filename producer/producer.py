import asyncio
from aiokafka import AIOKafkaProducer
import json

async def send_events():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        events = [
            {"user_id": 1, "item_id": 101, "event_type": "view"},
            {"user_id": 1, "item_id": 102, "event_type": "click"},
        ]
        for e in events:
            await producer.send_and_wait("user_events", json.dumps(e).encode())
            print(f"Sent: {e}")
    finally:
        await producer.stop()

asyncio.run(send_events())
