from fastapi.routing import APIRouter
from fastapi.requests import Request
from controllers.core.configs import settings
from views.admin.membro_admin import membro_admin
from datetime import datetime
from views.admin.area_admin import area_admin
from views.admin.autor_admin import autor_admin
from views.admin.duvida_admin import duvida_admin

router = APIRouter(prefix="/admin")
router.include_router(membro_admin.router, prefix="/admin")
router.include_router(area_admin.router,prefix='/admin')
router.include_router(autor_admin.router,prefix='/admin')
router.include_router(duvida_admin.router,prefix='/admin')


@router.get('/', name='admin_index')
async def admin_index(request: Request):
    context = {"request": request, "ano": datetime.now().year}
    return settings.TEMPLATES.TemplateResponse('admin/index.html', context=context)
