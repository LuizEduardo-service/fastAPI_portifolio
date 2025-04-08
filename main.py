from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from views.home_views import router
from views.admin.membro_admin import membro_admin
from views.admin import admin_view


app = FastAPI(redoc_url=None, docs_url=None)
app.mount('/media', StaticFiles(directory='media'), name='media')
app.mount('/static',StaticFiles(directory='static'), name='static')


app.include_router(router=router)
app.include_router(router=membro_admin.router)
app.include_router(router=admin_view.router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', reload=True, log_level='info', host='0.0.0.0', port=8000)