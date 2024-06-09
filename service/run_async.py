import asyncio
from typing import Coroutine, Any


def run_async(task: Coroutine[Any, Any, None]):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(task)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(task)
        loop.run_until_complete(task)