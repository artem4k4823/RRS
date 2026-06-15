import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api_v1.post import router as post_router
from app.api_v1.user import router as user_router
from app.api_v1.auth import router as auth_router
from app.api_v1.subscribtion import router as sub_router

app = FastAPI()

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


if __name__ == '__main__':
    uvicorn.run("main:app", port=8082, log_level='info', reload=True)
