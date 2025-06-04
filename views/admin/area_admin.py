
from datetime import datetime
from fastapi.routing import APIRouter
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException
from starlette.routing import Route

from controllers.core.configs import settings
from controllers.area_controller import AreaController
from views.admin.base_crud_view import BaseCrudView


class AreaAdmin(BaseCrudView):

    def __init__(self):

        super().__init__('area')

    async def object_list(self, request: Request):
        area_controller: AreaController = AreaController(request)
        return await super().object_list(object_controller = area_controller)
    
    async def create_object(self, request: Request):
        area_controller: AreaController = AreaController(request)

        if request.method == 'GET':
            context = {'request': area_controller.request, 'ano': datetime.now().year}
            return settings.TEMPLATES.TemplateResponse(f'admin/area/create.html', context=context)
        
        if request.method == 'POST':
            form = await request.form()
            dados: set = None

            try:
                await area_controller.post_crud()
            except ValueError as err:
                area: str = form.get('area')
                dados = {'area': area}
                context = {
                    'request': request,
                    'ano': datetime.now().year,
                    'error': err,
                    'objeto': dados
                }

                return settings.TEMPLATES.TemplateResponse('admin/area/create.html', context=context, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return RedirectResponse(request.url_for('area_list'), status_code=status.HTTP_302_FOUND)
    
    async def edit_object(self, request: Request):
        area_controller: AreaController = AreaController(request=request)
        area_id = request.path_params['objeto_id']

        if request.method == 'GET':
            return await super().detail_object(object_controller=area_controller, obj_id=area_id)
        
        if request.method == 'POST':
            area = await area_controller.get_one_crud(id_obj=area_id)

            if not area:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            form = await request.form()
            dados: set = None

            try:
                await area_controller.put_crud(obj=area)
            except ValueError as err:
                area: str = form.get('area')
                dados = {'area': area}
                context = {
                    'request': request,
                    'ano': datetime.now().year,
                    'error': err,
                    'objeto': dados
                }

                return settings.TEMPLATES.TemplateResponse('admin/area/edit.html', context= context)
            
            return RedirectResponse(request.url_for('area_list'),status_code=status.HTTP_302_FOUND)
        
        return await super().edit_object()
    
    async def object_delete(self, request: Request):
        area_controller: AreaController = AreaController(request)
        area_id: int = request.path_params['area_id']
        return await super().object_delete(object_id=area_id, object_controller=area_controller)

area_admin = AreaAdmin()