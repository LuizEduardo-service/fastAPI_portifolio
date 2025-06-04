from datetime import datetime
from typing import List
from models.autor_model import AutorModel
from models.tag_model import TagModel
from views.admin.base_crud_view import BaseCrudView
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from starlette.routing import Route
from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse

from controllers.post_controller import PostController
from controllers.core.configs import settings

class PostAdmin(BaseCrudView):

    def __init__(self):
        super().__init__('post')

    async def object_list(self, request: Request):
        post_controller: PostController = PostController(request=request)
        return await super().object_list(object_controller= post_controller)

    async def object_delete(self, request: Request):
        post_controller: PostController = PostController(request=request)
        post_id: int = request.path_params['objeto_id']

        return await super().object_delete(object_id= post_id, object_controller=post_controller)
    
    async def edit_object(self, request: Request):
        post_controller: PostController = PostController(request=request)
        post_id: int = request.path_params['objeto_id']

        if request.method == 'GET' and 'details' in str(post_controller.request.url):
            return await super().detail_object(obj_id=post_id,object_controller=post_controller)
        
        if request.method == 'GET' and 'edit' in str(post_controller.request.url):
            post = await post_controller.get_one_crud(id_obj=post_id)

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            autores = await post_controller.get_objetos(AutorModel)
            tags = await post_controller.get_objetos(TagModel)

            context = {'request': post_controller.request, 'ano': datetime.now().year, 'autores': autores, 'tags': tags, 'objeto': post}

            return settings.TEMPLATES.TemplateResponse(f'admin/post/edit.html', context=context)
        
        post = await post_controller.get_one_crud(id_obj=post_id)

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        

        form = await request.form()
        dados:set = None
        
        try:
            await post_controller.put_crud(obj=post)
        except ValueError as err:
            titulo: str = form.get('titulo')
            tags: list = form.getlist('tags')
            texto: str = form.get('texto')
            autor: str = form.get('autor')
            dados = {'id': post_id, 'titulo': titulo, 'tags': tags, 'texto': texto, 'autor':autor}
            context = {
                'request': request,
                'ano': datetime.now().year,
                'error': err,
                'objeto': dados
            }

            return settings.TEMPLATES.TemplateResponse(f'admin/post/edit.html', context=context)
        
        return RedirectResponse(request.url_for('post_list'), status_code=status.HTTP_302_FOUND)

    async def create_object(self, request: Request):
        post_controller: PostController = PostController(request=request)

        if request.method == 'GET':
            autores = await post_controller.get_objetos(AutorModel)
            tags = await post_controller.get_objetos(TagModel)
            context = {"request": post_controller.request, "ano": datetime.now().year, "autores": autores, "tags": tags}

            return settings.TEMPLATES.TemplateResponse(f"admin/post/create.html", context=context)

        form = request.form()
        dados:set = None

        try:
            await post_controller.post_crud()
        except ValueError as err:
            titulo: str = form.get('titulo')
            tags: List[object] = form.get('tags')
            texto: str = form.get('texto')
            autor: int = form.get('autor')
            dados = {"titulo": titulo, "tags": tags, "texto": texto, "autor": autor}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "objeto": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/post/create.html", context=context)
        return RedirectResponse(request.url_for('post_list'), status_code=status.HTTP_302_FOUND)


post_admin = PostAdmin()