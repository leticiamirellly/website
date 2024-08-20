import redis.asyncio as redis
import json
from typing import Callable
import os
import asyncio
from time import sleep
from asyncio import wait_for, TimeoutError
import async_timeout
import sys
sys.stdout.reconfigure(line_buffering=True)


from ragService import RagService

ragSrv = RagService()

class RedisSubscriber:
    def __init__(self):
        redis_host = os.getenv('REDIS_HOST')
        redis_port = os.getenv('REDIS_PORT')
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        self.channel = 'new_posts_channel'
        self.queue = asyncio.queues.Queue()
        
        
    async def start(self):
        await self.pubsub.subscribe(self.channel)
        print(f"Subscribed to Redis channel: {self.channel}")
        await asyncio.gather(self.handle_message(self.pubsub), self.get_data_and_send())
        
    async def stop(self):
        self.pubsub.unsubscribe(self.channel)
        print("Unsubscribed from Redis channel")

    async def handle_message(self, client):
        while True:
            message = await client.get_message()
            if message is not None:
                self.queue.put_nowait(message)
                print('Mensagem recebida')
            await asyncio.sleep(0.1)

    async def get_data_and_send(self):
        data = await self.queue.get()
        while True:
            if self.queue.empty():
                await asyncio.sleep(1)
            else:
                data = self.queue.get_nowait()
                await ragSrv.get_message(data)
            await asyncio.sleep(0.1)

            