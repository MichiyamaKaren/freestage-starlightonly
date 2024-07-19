import json
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from typing import Dict, Coroutine


class SSEConnection:
    def __init__(self, event_senders: Dict[str, Coroutine]) -> None:
        self.queue = asyncio.Queue()
        self.event_senders = event_senders

        for event in self.event_senders:
            self.create_event_sender_task(event)

    def create_event_sender_task(self, event: str):
        coro = self.event_senders[event]
        task = asyncio.create_task(coro())
        task.add_done_callback(lambda task: self.queue.put_nowait((event, task.result())))

    async def stream(self):
        while True:
            event, data = await self.queue.get()
            self.create_event_sender_task(event)
            yield f"event: {event}\ndata: {json.dumps(data)}\n\n"


class SSEBackend:
    def __init__(self, router: APIRouter, path: str) -> None:
        self.router = router
        self.path = path

        self.event_senders = {}
        self.connections = []

    def register(self, event: str):
        def wrapper(coro): 
            self.event_senders[event] = coro
            return coro
        return wrapper

    async def sse_endpoint(self):
        connection = SSEConnection(self.event_senders)
        return StreamingResponse(connection.stream(), media_type="text/event-stream")

    def router_register(self):
        self.router.add_api_route(self.path, self.sse_endpoint, methods=['GET'])
