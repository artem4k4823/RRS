from logging import info
import uvicorn
from fastapi import FastAPI
import uvicorn

from app.api_v1.post import router as post_router

app  = FastAPI()


@app.get('/')
def root():
    return 'hello world'


app.include_router(post_router)

if __name__ == '__main__':
    uvicorn.run("main:app", port = 8082, log_level='info', reload=True)
    

