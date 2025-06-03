from fastapi.requests import Request
from fastapi import UploadFile
from typing import List

from controllers.core.database import get_session
from models.autor_model import AutorModel
from controllers.base_controller import BaseController
from models.tag_model import TagModel


class AutorController(BaseController):
    def __init__(self, request: Request):
        super().__init__(request, AutorModel)

    async def post_crud(self):
        form = await self.request.form()

        nome: str = form.get('nome')
        imagem: UploadFile = form.get('imagem')
        tags: List[list] = form.getlist('tag')

        novo_nome = await self._upload_file(imagem=imagem, tipo='autor')
        autor: AutorModel = AutorModel(nome= nome, imagem = novo_nome)


        for id_tag in tags:
            tag = await self.get_objeto(TagModel, int(id_tag))
            autor.tags.append(tag)

        async with get_session() as session:
            session.add(autor)
            await session.commit()

    async def put_crud(self, obj: object):
        async with get_session() as session:
            autor: AutorModel = await session.get(AutorModel, obj.id)

            if autor:
                form = await self.request.form()

                nome: str = form.get('nome')
                imagem: UploadFile = form.get('imagem')
                tags: List[list] = form.getlist('tag')

                if nome and nome != autor.nome:
                    autor.nome = nome

                if tags:
                    autor.tags = []
                    await session.commit()

                    for id_tag in tags:
                        tag = await self.get_objeto(TagModel, int(id_tag))
                        autor.tags.append(tag)
                        # Operação para juntar o objeto tag que vem de outra
                        # sessão com o objeto autor que está nesta sessão.
                        tag_local = await session.merge(tag)
                        autor.tags.append(tag_local)
                if imagem.filename:
                    novo_nome = self._upload_file(imagem=imagem, tipo='autor')
                    autor.imagem = novo_nome

                await session.commit()



        
