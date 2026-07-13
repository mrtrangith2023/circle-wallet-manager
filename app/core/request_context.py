from contextvars import ContextVar

request_id_ctx = ContextVar(
    "request_id",
    default="-",
)

def get_request_id():

    return request_id_ctx.get()

def set_request_id(
    request_id: str,
):

    request_id_ctx.set(request_id)