from contextlib import asynccontextmanager
from sys import prefix
from fastapi import FastAPI


@asynccontextmanager
async def lifespan():
    pass

app = FastAPI(prefix='/auth', lifespan=lifespan)

