from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request


app = FastAPI(redoc_url=None, docs_url=None)
app.mount('/media', StaticFiles(directory='media'), name='media')
app.mount('/static',StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/', name='index')
async def ixdex(request: Request):
    return templates.TemplateResponse('home/index.html',context={"request": request})

@app.get('/about', name='about')
async def about(request: Request):
    return templates.TemplateResponse('about/about.html', context={"request": request})

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', reload=True, log_level='info', host='0.0.0.0')