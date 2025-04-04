from fastapi import APIRouter
from fastapi.requests import Request

from controllers.core.configs import settings

router = APIRouter()


@router.get('/', name='index')
async def ixdex(request: Request):
    return settings.TEMPLATES.TemplateResponse('home/index.html',context={"request": request})

@router.get('/about', name='about')
async def about(request: Request):
    return settings.TEMPLATES.TemplateResponse('home/about.html', context={"request": request})

@router.get('/faq', name='faq')
async def faq(request: Request):
    return settings.TEMPLATES.TemplateResponse('home/faq.html', context={"request": request})

@router.get('/pricing', name='pricing')
async def pricing(request: Request):
    return settings.TEMPLATES.TemplateResponse('home/pricing.html', context={"request": request})

@router.get('/contact', name='contact')
async def contact(request: Request):
    return settings.TEMPLATES.TemplateResponse('home/contact.html', context={"request": request})

@router.get('/blog', name='blog')
async def blog(request: Request):
    return settings.TEMPLATES.TemplateResponse('home/blog.html', context={"request": request})


@router.get('/blog_post', name='blog_post')
async def blog_post(request: Request):
    return settings.TEMPLATES.TemplateResponse('home/blog_post.html', context={"request": request})


@router.get('/portfolio_item', name='portfolio_item')
async def portfolio_item(request: Request):
    return settings.TEMPLATES.TemplateResponse('home/portfolio_item.html', context={"request": request})

@router.get('/portfolio', name='portfolio')
async def portifolio(request: Request):
    return settings.TEMPLATES.TemplateResponse('home/portfolio.html', context={"request": request})

