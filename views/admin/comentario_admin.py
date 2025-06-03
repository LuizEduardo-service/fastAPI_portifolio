from datetime import datetime
from models.post_model import PostModel
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
    
    async def object_delete(self, request: Request):
        comentario_controller: ComentarioController = ComentarioController(request=request)
        comentario_id = request.path_params['objeto_id']
        return await super().object_delete(object_id=comentario_id, object_controller=comentario_controller)
    
    async def create_object(self, request: Request):
        comentario_controller: ComentarioController = ComentarioController(request=request)

        if request.method == 'GET':
            posts = await comentario_controller.get_objetos(PostModel)
            context ={'request':comentario_controller.request, 'ano': datetime.now().year, 'posts': posts}
            return settings.TEMPLATES.TemplateResponse(f"admin/comentario/create.html", context=context)

        form = await request.form()
        dados: set = None

        try:
            await comentario_controller.post_crud()
        except ValueError as err:
            id_post: int = form.get('id_post')
            autor: str = form.get('autor')
            texto: str = form.get('texto')
            posts = await comentario_controller.get_objetos(PostModel)
            dados = {"id_post": id_post, "autor": autor, "texto": texto}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "posts": posts,
                "objeto": dados
            }

            return settings.TEMPLATES.TemplateResponse('admin/comentario/create.html', context=context)


        return RedirectResponse(request.url_for('comentario_list'),status_code=status.HTTP_302_FOUND)
    

    async def edit_object(self, request: Request):
        comentario_controller: ComentarioController = ComentarioController(request=request)
        comentario_id: int = request.path_params['objeto_id']

        if request.method == 'GET' and 'details' in str(comentario_controller.request.url):
            return await super().detail_object(object_controller=comentario_controller, obj_id=comentario_id)

        if request.method == 'GET' and 'edit' in str(comentario_controller.request.url):
            comentario = await comentario_controller.get_one_crud(id_obj=comentario_id)

            if not comentario:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            posts = await comentario_controller.get_objetos(PostModel)
            context = {'request': comentario_controller.request, 'ano': datetime.now().year, 'posts': posts, 'objeto': comentario}
            return settings.TEMPLATES.TemplateResponse('admin/comentario/edit.html', context=context) 

        comentario = await comentario_controller.get_one_crud(id_obj=comentario_id)

        if not comentario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        form = await request.form()
        dados: set = None

        try:
            await comentario_controller.put_crud(obj=comentario)
        except ValueError as err:
            post: int = form.get('post')
            autor: str = form.get('autor')
            texto: str = form.get('texto')
            dados = {"id": comentario_id, 'post': post, 'autor:': autor, 'texto': texto}
            context = {
                'request': request,
                'ano': datetime.now().year,
                'error': err,
                'objeto': dados
            }

            return settings.TEMPLATES.TemplateResponse('admin/comentario/edit.html', context=context)
        
        return RedirectResponse(request.url_for('comentario_list'), status_code=status.HTTP_302_FOUND)


comentario_admin = ComentarioAdmin()