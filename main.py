from logging import info
import uvicorn
from fastapi import FastAPI
import uvicorn

app  = FastAPI()


@app.get('/')
def root():
    return 'hello world'


if __name__ == '__main__':
    uvicorn.run("main:app", port = 8082, log_level='info', reload=True)
    

