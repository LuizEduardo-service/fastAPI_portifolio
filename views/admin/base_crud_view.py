from datetime import datetime
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRoute
from starlette.routing import Route
from controllers.core.configs import settings
from fastapi.responses import RedirectResponse, Response
from controllers.base_controller import BaseController
from fastapi import APIRouter, status
from starlette.routing import Route
from controllers.core.deps import valida_login


class BaseCrudView:

    def __init__(self, template_base: str) -> None:
        self.template_base = template_base
        self.router = APIRouter()
        self.router.routes.append(APIRoute(path=f'/{self.template_base}/list', endpoint=self.object_list, methods=['GET'], name=f'{self.template_base}_list'))
        self.router.routes.append(APIRoute(path=f'/{self.template_base}/create', endpoint=self.create_object, methods=['GET', 'POST'], name=f'{self.template_base}_create'))
        self.router.routes.append(APIRoute(path=f'/{self.template_base}/details/' +' {objeto_id:int}', endpoint=self.edit_object, methods=['GET'], name=f'{self.template_base}_details'))
        self.router.routes.append(APIRoute(path=f'/{self.template_base}/edit/' + '{objeto_id:int}',endpoint=self.edit_object,methods=['GET', 'POST'], name=f'{self.template_base}_edit'))
        self.router.routes.append(Route(path=f'/{self.template_base}/delete/' +' {objeto_id:int}', endpoint=self.object_delete,methods=['POST'],name=f'{self.template_base}_delete'))

    async def create_object(self) -> Response:
        """Rota de carregamento de template"""
        raise NotImplementedError("Metodo não implentado")
    
    async def edit_object(self) -> Response:
        """rota para edicao de template"""
        raise NotImplementedError("Metodo não implentado")

    async def object_list(self, object_controller: BaseController) -> Response:
        """Listar dados do objeto"""

        context = valida_login(request=object_controller.request)

        if not context.get('membro'):
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        
        dados = await object_controller.get_all()
        context.update({"objeto": dados})

        return settings.TEMPLATES.TemplateResponse(f'admin/{self.template_base}/list.html', context=context)
    
    async def object_delete(self, object_id: int, object_controller: BaseController) -> Response:
        """remove objeto"""

        context = valida_login(request=object_controller.request)

        if not context.get('membro'):
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        
        obj = await object_controller.get_one_crud(id_obj=object_id)

        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        object_controller.delete_crud(id_obj=obj.id)

        return Response(object_controller.request.url_for(f'{self.template_base}_list'))
    
    async def detail_object(self, object_controller: BaseController, obj_id: int) -> Response:
        """Consulta um objeto por id"""

        context = valida_login(request=object_controller.request)

        if not context.get('membro'):
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)

        obj = await object_controller.get_one_crud(id_obj=obj_id)

        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        context = {"request": object_controller.request, "ano": datetime.now().year, "objeto": obj}

        if 'details' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f'admin/{self.template_base}/details.html', context=context)
        
        if 'edit' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f'admin/{self.template_base}/edit.html', context=context)

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)