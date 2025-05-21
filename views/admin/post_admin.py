from views.admin.base_crud_view import BaseCrudView
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from starlette.routing import Route
from fastapi.routing import APIRouter

from controllers.post_controller import PostController
from controllers.core.configs import settings

class PostAdmin(BaseCrudView):

    def __init__(self):
        self.router = APIRouter()
        self.router.routes.append(Route(path='/post/list', endpoint=self.object_list, methods=['GET'], name='post_list'))
        self.router.routes.append(Route(path='/post/create', endpoint=self.create_object, methods=['GET', 'POST'], name='post_create'))
        self.router.routes.append(Route(path='/post/details/{post_id:int}', endpoint=self.edit_object,methods=['GET'], name='post_details'))
        self.router.routes.append(Route(path='/post/edit/{post_id:int}', endpoint=self.edit_object, methods=['GET', 'POST'],name='post_edit'))
        self.router.routes.append(Route(path='/post/delete/{post_id:int}',endpoint=self.object_delete, methods=['DELETE'], name='post_delete'))
        super().__init__('post')

    async def object_list(self, request: Request):
        post_controller: PostController = PostController(request=request)
        return await super().object_list(object_controller= post_controller)