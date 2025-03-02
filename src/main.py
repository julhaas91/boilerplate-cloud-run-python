import os
import json
from litestar import Litestar, Request, get, post
from common import logger


env = os.environ.get("PYTHON_ENV")


@post("/process")
async def process_message(request: Request) -> dict:
    data = await request.json()
    message = data.get("message", "")
    return {"uppercaseMessage": message.upper()}

@get("/health")
async def health_check() -> str:
    """Check service health."""
    logger.info("Health check route called.")
    return json.dumps({"status": "ok"})


app = Litestar(
    route_handlers=[process_message, health_check]
)
