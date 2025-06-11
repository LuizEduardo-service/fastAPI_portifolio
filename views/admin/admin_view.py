from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi import status
from controllers.core.configs import settings
from views.admin.membro_admin import membro_admin
from datetime import datetime
from views.admin.area_admin import area_admin
from views.admin.autor_admin import autor_admin
from views.admin.duvida_admin import duvida_admin
from views.admin.comentario_admin import comentario_admin
from views.admin.post_admin import post_admin
from views.admin.projeto_admin import projeto_admin
from views.admin.tag_admin import tag_admin
from controllers.core.auth import get_membro_id
from controllers.membro_controller import MembroController
from fastapi.exceptions import HTTPException


router = APIRouter(prefix="/admin")
router.include_router(membro_admin.router)
router.include_router(area_admin.router)
router.include_router(autor_admin.router)
router.include_router(duvida_admin.router)
router.include_router(comentario_admin.router)
router.include_router(post_admin.router)
router.include_router(projeto_admin.router)
router.include_router(tag_admin.router)

@router.get('/', name='admin_index')
async def admin_index(request: Request):
    membro_id: int = get_membro_id(request=request)

    context = {"request": request, "ano": datetime.now().year}
    
    if membro_id and membro_id > 0: 

        membro_controller: MembroController = MembroController(request=request)
        membro = await membro_controller.get_one_crud(membro_id)

        if not membro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        context.update({'membro': membro})
        return settings.TEMPLATES.TemplateResponse('admin/index.html', context=context)
    
    return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
