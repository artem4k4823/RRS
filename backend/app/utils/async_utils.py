import asyncio
from fastapi import HTTPException, status
from rabbitmq.rabbitmq import pending_requests

async def wait_for_xml_response(task_id: str, future: asyncio.Future, timeout: float = 30.0):
    try:
        xml_content = await asyncio.wait_for(future, timeout=timeout)
        return xml_content
    except asyncio.TimeoutError:
        raise HTTPException(status.HTTP_504_GATEWAY_TIMEOUT, detail="Timeout waiting for generator service")
    finally:
        pending_requests.pop(task_id, None)