from datetime import datetime
from controllers.core.deps import valida_login
from models.tag_model import TagModel
from views.admin.base_crud_view import BaseCrudView
from fastapi.requests import Request
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from starlette.routing import Route

from controllers.core.configs import settings
from controllers.tag_controller import TagController

class TagAdmin(BaseCrudView):

    def __init__(self):
        super().__init__('tag')

    async def object_list(self, request: Request):
        tag_controller: TagController = TagController(request=request)
        return await super().object_list(object_controller=tag_controller)
    
    async def object_delete(self,request: Request):
        tag_controller: TagController = TagController(request=request)
        tag_id:int = request.path_params['objeto_id']
        return await super().object_delete(object_id= tag_id, object_controller= tag_controller)
    
    async def create_object(self, request:Request):

        context = await valida_login(request=request)

        if not context.get('membro'):
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        
        tag_controller:TagController = TagController(request= request)
        form = await request.form()
        dados: set = None

        if request.method == 'GET':
            # Adicionar o request no context
            context = {"request": tag_controller.request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/tag/create.html", context=context)

        try:
            await tag_controller.post_crud()
        except ValueError as err:
            dados = {
                'tag': form.get('tag')
            }
            context.update({
                'error': err,
                'objeto': dados
            })

            return settings.TEMPLATES.TemplateResponse('/admin/tag/create.html', context=context)
        
        return RedirectResponse(request.url_for('tag_list'), status_code=status.HTTP_302_FOUND)
    
    async def edit_object(self, request: Request):

        context = await valida_login(request=request)

        if not context.get('membro'):
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        
        tag_controller: TagController = TagController(request=request)
        tag_id: int = request.path_params['objeto_id']

        if request.method == 'GET':
            return await super().detail_object(obj_id=tag_id, object_controller=tag_controller)


        tag: TagModel = await tag_controller.get_one_crud(id_obj=tag_id)

        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        form = await request.form()
        dados:set = None

        try:
            await tag_controller.put_crud(tag)
        except ValueError as err:
            dados = {
                'id': tag_id,
                'tag': form.get()
            }
            context.update({
                'error': err,
                'objeto': dados
            })

            return settings.TEMPLATES.TemplateResponse('/admin/tag/edit.html', context=context)
        
        return RedirectResponse(request.url_for('tag_list'), status_code=status.HTTP_302_FOUND)



tag_admin = TagAdmin()