from contextvars import ContextVar

user_context: ContextVar[str | None] = ContextVar("user_context", default="anonymous")
client_ip_context: ContextVar[str | None] = ContextVar("client_ip_context", default="anonymous")