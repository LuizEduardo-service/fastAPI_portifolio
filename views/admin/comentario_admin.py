from views.admin.base_crud_view import BaseCrudView
from fastapi.routing import APIRouter
from starlette.routing import Route
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from controllers.comentario_controller import ComentarioController
from controllers.core.configs import settings
from fastapi.requests import Request

class ComentarioAdmin(BaseCrudView):

    def __init__(self):
        self.router = APIRouter()
        self.router.routes.append(Route('/comentario/list',endpoint=self.object_list, methods=['GET'], name='comentario_list'))
        self.router.routes.append(Route(path='/comentario/create', endpoint=self.create_object, methods=['GET', 'POST'], name='comentario_create'))
        self.router.routes.append(Route(path='/comentario/details/{comentario_id:int}',endpoint=self.edit_object, methods=['GET'],name='comentario_details'))
        self.router.routes.append(Route(path='/comentario/edit/{comentario_id:int}', endpoint=self.edit_object,methods=['GET', 'POST'],name='comentario_edit'))
        self.router.routes.append(Route(path='/comentario/delete/{comentario_id:int}', endpoint=self.object_delete, methods='DELETE',name='comentario_delete'))
        super().__init__('comentario')

    async def object_list(self, request: Request):
        comentario_controller: ComentarioController = ComentarioController(request)
        return await super().object_list(object_controller=comentario_controller)