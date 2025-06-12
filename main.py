from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from views import home_views, error_view
from views.admin import admin_view

from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


middlewares = [
      Middleware(TrustedHostMiddleware, allowed_hosts=['localhost', 'fapid.testeapi.com.br']),
    # Middleware(HTTPSRedirectMiddleware) # usar apenas em produção quando houver um certificado digital
]

app = FastAPI(redoc_url=None, docs_url=None, exception_handlers=error_view.exception_handlers, middleware=middlewares)
app.include_router(router=home_views.router)
app.include_router(router=admin_view.router)

app.mount('/static',StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')



if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', reload=True, log_level='info', host='0.0.0.0', port=8000)