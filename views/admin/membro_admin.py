from datetime import datetime

from fastapi.routing import APIRouter
from starlette.routing import Route
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response,RedirectResponse
from fastapi.exceptions import HTTPException

from controllers.core.configs import settings
from controllers.core.deps import valida_login
from controllers.membro_controller import MembroController
from views.admin.base_crud_view import BaseCrudView


class MembroAdmin(BaseCrudView):

    def __init__(self):
        super().__init__('membro')

    async def object_list(self, request: Request):
        membro_controller: MembroController = MembroController(request)
        return await super().object_list(object_controller = membro_controller)
    
    async def delete_object(self, request: Request):
        membro_controller: MembroController = MembroController(request)
        membro_id: int = request.path_params['objeto_id']
        return await super().object_delete(object_id=membro_id, object_controller = membro_controller)
    
    async def create_object(self,request: Request):

        context = valida_login(request=request)

        if not context.get('membro'):
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        
        membro_controller: MembroController = MembroController(request)

        if request.method == 'GET':
            context = {"request": membro_controller.request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f'admin/membro/create.html', context=context)
        
        if request.method == 'POST':
            form = await request.form()
            dados: set = None

            try:
                await membro_controller.post_crud()
            except ValueError as err:
                nome: str = form.get('nome')
                senha: str = form.get('senha')
                email: str = form.get('email')
                funcao: str = form.get('funcao')
                dados = {"nome": nome,
                         "funcao": funcao,
                         "email": email,
                         "senha": senha
                         }
                context.update({
                    'error': err,
                    'objeto': dados
                })

                return settings.TEMPLATES.TemplateResponse('admin/membro/create.html', context=context,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return RedirectResponse(request.url_for("membro_list"), status_code=status.HTTP_302_FOUND)
        
    async def edit_object(self, request: Request):

        context = valida_login(request=request)

        if not context.get('membro'):
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        membro_controller: MembroController = MembroController(request)
        membro_id = request.path_params['objeto_id']

        if request.method == 'GET':
            return await super().detail_object(object_controller=membro_controller, obj_id= membro_id )
        
        if request.method == 'POST':
            membro = await membro_controller.get_one_crud(id_obj=membro_id)

            if not membro:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            form = await request.form()
            dados: set = None
            try:
                await membro_controller.put_crud(obj=membro)

            except ValueError as err:
                nome: str = form.get('nome')
                senha: str = form.get('senha')
                email: str = form.get('email')
                funcao: str = form.get('funcao')
                dados = {"id": membro_id, 
                         "nome": nome, 
                         "senha": senha, 
                         "email": email, 
                         "funcao": funcao}
                context.update({
                    'error': err,
                    'objeto': dados
                })

                return settings.TEMPLATES.TemplateResponse('admin/membro/edit.html', context=context)
            
            return RedirectResponse(request.url_for('membro_list'), status_code=status.HTTP_302_FOUND)



        return await super().edit_object()
    
membro_admin = MembroAdmin()