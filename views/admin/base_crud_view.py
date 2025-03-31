from datetime import datetime
from fastapi.exceptions import HTTPException
from controllers.core.configs import settings
from fastapi.responses import Response
from controllers.base_controller import BaseController
from fastapi import status


class BaseCrudView:

    def __init__(self, template_base: str) -> None:
        self.template_base = template_base

    async def create_object(self) -> Response:
        """Rota de carregamento de template"""
        raise NotImplementedError("Metodo não implentado")
    
    async def edit_object(self) -> Response:
        """rota paara edicao de template"""
        raise NotImplementedError("Metodo não implentado")

    async def object_list(self, object_controller: BaseController) -> Response:
        """Listar dados do objeto"""

        dados = await object_controller.get_all()
        context = {"request": object_controller.request, "ano": datetime.now().year,"dados": dados}

        return settings.TEMPLATES.TemplateResponse(f'admin/{self.template_base}/list.html', context=context)
    
    async def delete_object(self, object_id: int, object_controller: BaseController) -> Response:
        """remove objeto"""
        obj = await object_controller.get_one_crud(object_id)

        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        object_controller.delete_crud(obj.id)

        return Response(object_controller.request.url_for(f'{self.template_base}_list'))
    

    async def detail_object(self, object_controller: BaseController, obj_id: int) -> Response:
        """Consulta um objeto por id"""

        obj = await object_controller.get_one_crud(id_obj=obj_id)

        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        context = {"request": object_controller.request, "ano": datetime.now().year, "objeto": obj}

        if 'details' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f'admin/{self.template_base}/datail.html', context=context)
        
        if 'edit' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f'admin/{self.template_base}/edit.html', context=context)

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)