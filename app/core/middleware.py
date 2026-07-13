import time
import uuid

from fastapi import Request

from app.core.logger import logger
from app.core.request_context import set_request_id


async def log_requests(
    request: Request,
    call_next,
):
    request_id = str(uuid.uuid4())

    set_request_id(request_id)

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (
        time.perf_counter() - start_time
    ) * 1000

    client = (
        request.client.host
        if request.client
        else "-"
    )

    logger.info(
        "event=http_request "
        "method=%s "
        "path=%s "
        "status=%s "
        "duration_ms=%.2f "
        "client=%s",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
        client,
    )

    response.headers[
        "X-Request-ID"
    ] = request_id

    return response