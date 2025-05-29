from controllers.base_controller import BaseController
from models.projeto_model import ProjetoModel
from controllers.core.database import get_session
from fastapi import UploadFile



class ProjetoController(BaseController):

    def __init__(self, request):
        super().__init__(request, ProjetoModel)

    async def post_crud(self):
        form = await self.request.form()

        titulo: str = form.get('titulo')
        descricao_inicial: str = form.get('descricao_inicial')
        imagem1: UploadFile = form.get('imagem1')
        imagem2: UploadFile = form.get('imagem2')
        imagem3: UploadFile = form.get('imagem3')
        descricao_final: str = form.get('descricao_final')

        novo_imagem1 = await self._upload_file(imagem=imagem1, tipo='projeto')
        novo_imagem2 = await self._upload_file(imagem=imagem2, tipo='projeto')
        novo_imagem3 = await self._upload_file(imagem=imagem3, tipo='projeto')

        projeto: ProjetoModel = ProjetoModel(titulo=titulo,
                                            descricao_inicial=descricao_inicial,
                                            descricao_final= descricao_final,
                                            imagem1=novo_imagem1,
                                            imagem2=novo_imagem2,
                                            imagem3=novo_imagem3,
                                            link='teste'
                                                )
        
        async with get_session() as session:
            session.add(projeto)
            await session.commit()

    async def put_crud(self, obj):

        async with get_session() as session:
            projeto: ProjetoModel = await session.get(self.model, obj.id)
            form = await self.request.form()

            titulo: str = form.get('titulo')
            descricao_inicial: str = form.get('descricao_inicial')
            imagem1: UploadFile = form.get('imagem1')
            imagem2: UploadFile = form.get('imagem2')
            imagem3: UploadFile = form.get('imagem3')
            descricao_final: str = form.get('descricao_final')

            if titulo and titulo != projeto.titulo:
                projeto.titulo = titulo
            if descricao_final and descricao_final != projeto.descricao_final:
                projeto.descricao_final = descricao_final
            if descricao_inicial and descricao_inicial != projeto.descricao_inicial:
                projeto.descricao_inicial = descricao_inicial
            if imagem1.filename:
                imagem1_novo = await self._upload_file(imagem=imagem1, tipo='projeto')
                projeto.imagem1 = imagem1_novo
            if imagem2.filename:
                imagem2_novo = await self._upload_file(imagem=imagem2, tipo='projeto')
                projeto.imagem2 = imagem2_novo
            if imagem3.filename:
                imagem3_novo = await self._upload_file(imagem=imagem3, tipo='projeto')
                projeto.imagem3 = imagem3_novo

            await session.commit()

