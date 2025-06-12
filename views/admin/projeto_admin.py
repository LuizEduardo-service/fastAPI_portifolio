from datetime import datetime
from controllers.core.deps import valida_login
from views.admin.base_crud_view import BaseCrudView
from fastapi.requests import Request
from fastapi.routing import APIRouter
from starlette.routing import Route
from fastapi import status
from fastapi.exceptions import HTTPException
from models.projeto_model import ProjetoModel
from controllers.core.configs import settings
from fastapi.responses import RedirectResponse

from controllers.projeto_controller import ProjetoController


class ProjetoAdmin(BaseCrudView):
    
    def __init__(self):
        super().__init__('projeto')

    async def object_list(self, request: Request):
        projeto_controller: ProjetoController = ProjetoController(request=request)
        return await super().object_list(object_controller=projeto_controller)
    
    async def object_delete(self,request: Request):
        projeto_controller: ProjetoController = ProjetoController(request= request)
        projeto_id: int = request.path_params['objeto_id']

        return await super().object_delete(object_id=projeto_id, object_controller= projeto_controller)
    
    async def edit_object(self, request: Request):
        
        context = await valida_login(request=request)

        if not context.get('membro'):
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        
        projeto_controller: ProjetoController = ProjetoController(request=request)
        projeto_id: int = int(request.path_params['objeto_id'])

        if request.method == 'GET':
            return await super().detail_object(object_controller=projeto_controller, obj_id=projeto_id)
        

        projeto = await projeto_controller.get_one_crud(id_obj=projeto_id)

        if not projeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


        form = await request.form()
        dados:set = None

        try:
            await projeto_controller.put_crud(obj=projeto)
        except Exception as err:
            dados = {
                'id':projeto_id,
                'titulo': form.get('titulo'),
                'descricao_inicial': form.get('descricao_inicial'),
                'descricao_final': form.get('descricao_final')
            }
            context.update({
                'error': err,
                'objeto': dados
            })
            return settings.TEMPLATES.TemplateResponse('/admin/projeto/edit.html', context=context)
        
        return RedirectResponse(request.url_for('projeto_list'), status_code=status.HTTP_302_FOUND)

    async def create_object(self, request: Request):
        projeto_controller:ProjetoController = ProjetoController(request=request)

        if request.method == 'GET':
            context = {'request': projeto_controller.request, 'ano': datetime.now().year}
            return settings.TEMPLATES.TemplateResponse('/admin/projeto/create.html', context=context)
        
        
        form = await request.form()
        dados: set = None
        try:
            await projeto_controller.post_crud()
        except ValueError as err:
            dados = {
                'titulo': form.get('titulo'),
                'descricao_inicial': form.get('descricao_inicial'),
                'descricao_final': form.get('descricao_final')
            }
            context = {
                'request': request,
                'ano': datetime.now().year,
                'error': err,
                'objeto': dados
                
            }

            return settings.TEMPLATES.TemplateResponse('/admin/projeto/create.html', context=context)
        
        return RedirectResponse(request.url_for('projeto_list'), status_code=status.HTTP_302_FOUND)
            


projeto_admin = ProjetoAdmin()
