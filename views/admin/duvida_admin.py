from datetime import datetime
from controllers.duvida_controller import DuvidaController
from controllers.area_controller import AreaController
from models.area_model import AreaModel
from views.admin.base_crud_view import BaseCrudView


from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from starlette.routing import Route
from controllers.core.configs import settings
from fastapi import status

class DuvidaAdmin(BaseCrudView):

    def __init__(self):
        super().__init__('duvida')

    async def object_list(self, request: Request):
        duvida_controller: DuvidaController = DuvidaController(request)
        return await super().object_list(object_controller= duvida_controller)
    
    async def object_delete(self, request: Request):
        duvida_controller: DuvidaController = DuvidaController(request)
        duvida_id = request.path_params['objeto_id']

        return await super().object_delete(object_id=duvida_id, object_controller=duvida_controller)

    async def create_object(self, request: Request):
        duvida_controller: DuvidaController = DuvidaController(request)

        if request.method == 'GET':
            areas = await duvida_controller.get_objetos(AreaModel)
            context = {'request': duvida_controller.request, 'ano': datetime.now().year, "areas": areas}
            return settings.TEMPLATES.TemplateResponse('/admin/duvida/create.html', context=context)
        
        form = await request.form()
        dados: str = None

        try:
            await duvida_controller.post_crud()
        except ValueError as err:
            id_area = form.get('area')
            titulo: str = form.get('tutulo')
            resposta: str = form.get('resposta')
            dados = {
                'id_area': id_area,
                'titulo': titulo,
                'resposta': resposta
            }
            context = {
                'request': request,
                'ano': datetime.now().year,
                'error': err,
                'objeto': dados
            }
            return settings.TEMPLATES.TemplateResponse('admin/duvida/create.html', context=context)
        
        return RedirectResponse(request.url_for('duvida_list'), status_code=status.HTTP_302_FOUND)

    async def edit_object(self, request: Request):
        duvida_controller: DuvidaController = DuvidaController(request)
        duvida_id: int = request.path_params['objeto_id']
        duvida = await duvida_controller.get_one_crud(id_obj=duvida_id)

        if not duvida:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Registro não encontrado.')
        
        if request.method == 'GET' and 'details' in str(duvida_controller.request.url):
            return await super().detail_object(obj_id=duvida_id, object_controller=duvida_controller)
        
        if request.method == 'GET' and 'edit' in str(duvida_controller.request.url):
            areas = await duvida_controller.get_objetos(AreaModel)
            context = {'request': duvida_controller.request, 'ano': datetime.now().year, 'objeto': duvida, 'areas': areas}
            return settings.TEMPLATES.TemplateResponse(f'admin/duvida/edit.html', context=context)

        form = await request.form()
        dados: set = None

        try:
            await duvida_controller.put_crud(obj=duvida)
        except ValueError as err:
            area_id: int = form.get('area')
            titulo: str = form.get('titulo')
            resposta: str = form.get('resposta')
            dados = {'id': area_id, 'titulo': titulo, 'resposta': resposta}
            context = {
                'request': request,
                'ano':datetime.now().year,
                'error': err,
                'objeto': dados
            }

            return settings.TEMPLATES.TemplateResponse('admin/duvida/edit.html', context=context)
        
        return RedirectResponse(request.url_for('duvida_list'),status_code=status.HTTP_302_FOUND)


duvida_admin = DuvidaAdmin()