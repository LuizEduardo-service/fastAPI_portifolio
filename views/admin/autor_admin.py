
from datetime import datetime
from typing import List
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from starlette.routing import Route
from models.tag_model import TagModel
from views.admin.base_crud_view import BaseCrudView
from fastapi import status
from fastapi.exceptions import HTTPException

from controllers.core.configs import settings
from controllers.autor_controller import AutorController

class AutorAdmin(BaseCrudView):

    def __init__(self):
        # self.router = APIRouter()
        # self.router.routes.append(Route(path='/autor/list', endpoint=self.object_list,methods=['GET'] ,name='autor_list'))
        # self.router.routes.append(Route(path='/autor/create', endpoint=self.create_object, methods=['GET', 'POST'], name='autor_create'))
        # self.router.routes.append(Route(path='/autor/details/{autor_id:int}', endpoint=self.edit_object, methods=['GET'], name='autor_details'))
        # self.router.routes.append(Route(path='/autor/edit/{autor_id:int}', endpoint=self.edit_object, methods=['GET', 'POST'], name='autor_edit'))
        # self.router.routes.append(Route(path='/autor/delete/{autor_id:int}', endpoint=self.object_delete, methods=['DELETE'], name='autor_delete'))
        super().__init__('autor')

    async def object_list(self, request: Request):
        autor_controller: AutorController = AutorController(request)
        return await super().object_list(object_controller=autor_controller)
    
    async def object_delete(self, request: Request):
        autor_controller: AutorController = AutorController(request)
        autor_id = request.path_params['objeto_id']
        return await super().object_delete(object_id=autor_id, object_controller=autor_controller)

    async def edit_object(self, request:Request):
        autor_controller: AutorController = AutorController(request)
        autor_id = request.path_params['objeto_id']


        autor = await autor_controller.get_one_crud(id_obj=autor_id)
        if not autor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET' and 'details' in str(autor_controller.request.url):
            return await super().detail_object(object_controller=autor_controller, obj_id=autor_id)
        
        if request.method == 'GET' and 'edit' in str(autor_controller.request.url):
    
            tags = await autor_controller.get_objetos(TagModel)
            context = {'request': autor_controller.request, 'ano': datetime.now().year, 'objeto': autor,'tags': tags}
            return settings.TEMPLATES.TemplateResponse('admin/autor/edit.html',context=context)

        form = await request.form()
        dados: set = None

        try:
            autor_controller.put_crud(autor)
        except ValueError as err:
            nome = form.get('nome')
            tags: List[list] = form.getlist('tags')
            dados = {'nome': nome, 'tags': tags}
            context = {
                'request': request,
                'ano': datetime.now().year,
                'error': err,
                'objeto': dados
            }
            return settings.TEMPLATES.TemplateResponse('admin/autor/edit.html', context=context)
        
        return RedirectResponse(request.url_for('autor_list'),status_code=status.HTTP_302_FOUND)

    async def create_object(self, request: Request):
        autor_controller: AutorController = AutorController(request)

        if request.method == 'GET':
            tags = await autor_controller.get_objetos(TagModel)
            context = {'request': autor_controller.request, 'ano': datetime.now().year, 'tags': tags}

            return settings.TEMPLATES.TemplateResponse(f'admin/autor/create.html', context=context)

        form = await request.form()
        dados: set = None

        try:
            await autor_controller.post_crud()
        except ValueError as err:
            nome: str = form.get('nome')
            tags: List[list] = form.get('tag')
            dados = {'nome': nome, 'tags': tags}
            context = {
                'request': request,
                'ano': datetime.now().year,
                'error': err,
                'objeto': dados
            }

            return settings.TEMPLATES.TemplateResponse('admin/autor/create.html', context=context)
        
        return RedirectResponse(request.url_for('autor_list'), status_code=status.HTTP_302_FOUND)
    
autor_admin = AutorAdmin()