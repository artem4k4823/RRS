import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from prometheus_fastapi_instrumentator import Instrumentator

from sqladmin import Admin, ModelView
from app.core.models.Admin import UserAdmin,PostAdmin,SubscriptionAdmin
from app.auth.Adminauth.admin_auth import authentication_backend

from app.core.database import db

from rabbitmq.rabbitmq import RabbitMQ

from app.core.config import settings

from app.api_v1.post import router as post_router
from app.api_v1.user import router as user_router
from app.api_v1.auth import router as auth_router
from app.api_v1.subscribtion import router as sub_router
from app.api_v1.parser import router as parser_router

rabbitmq = RabbitMQ(settings.RABBIT_URL)

@asynccontextmanager
async def lifespan(app:FastAPI):
    connection = await rabbitmq.connect()
    channel = await connection.channel()
    post_exchange = await rabbitmq.declare_post_excange(channel)
    await rabbitmq.declare_post_queue(channel,post_exchange)
    app.state.post_exchange = post_exchange
    
    yield
    await connection.close()

app = FastAPI(lifespan=lifespan)

admin = Admin(app, db.engine, authentication_backend = authentication_backend)


# ── Prometheus metrics (/metrics endpoint) ───────────────────────
Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=False,
    excluded_handlers=["/metrics", "/health"],
    env_var_name="ENABLE_METRICS",
).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)


@app.get('/')
def root():
    return 'hello world'


@app.get('/health')
def health():
    return {"status": "ok"}


app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(sub_router)
app.include_router(parser_router)

admin.add_view(UserAdmin)
admin.add_view(PostAdmin)
admin.add_view(SubscriptionAdmin)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8082, log_level='info', reload=True)
