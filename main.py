from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI(redoc_url=None, docs_url=None)
app.mount('/media', StaticFiles(directory='media'), name='media')
app.mount('/static',StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', reload=True, log_level='info', host='0.0.0.0')