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
    return templates.TemplateResponse('home/about.html', context={"request": request})

@app.get('/faq', name='faq')
async def faq(request: Request):
    return templates.TemplateResponse('home/faq.html', context={"request": request})

@app.get('/pricing', name='pricing')
async def pricing(request: Request):
    return templates.TemplateResponse('home/pricing.html', context={"request": request})

@app.get('/contact', name='contact')
async def contact(request: Request):
    return templates.TemplateResponse('home/contact.html', context={"request": request})

@app.get('/blog', name='blog')
async def blog(request: Request):
    return templates.TemplateResponse('home/blog.html', context={"request": request})


@app.get('/blog_post', name='blog_post')
async def blog_post(request: Request):
    return templates.TemplateResponse('home/blog_post.html', context={"request": request})


@app.get('/portfolio_item', name='portfolio_item')
async def portfolio_item(request: Request):
    return templates.TemplateResponse('home/portfolio_item.html', context={"request": request})

@app.get('/portfolio', name='portfolio')
async def portifolio(request: Request):
    return templates.TemplateResponse('home/portfolio.html', context={"request": request})

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', reload=True, log_level='info', host='0.0.0.0')