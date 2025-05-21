from typing import List
from fastapi.requests import Request
from fastapi import UploadFile

from controllers.core.database import get_session
from models.post_model import PostModel
from controllers.base_controller import BaseController


class PostController(BaseController):
    def __init__(self, request: Request):
        super().__init__(request, PostModel)

    async def post_crud(self):
        form = await self.request.form()

        titulo: str = form.get('titulo')
        tags: str = form.getlist('tags')
        imagem: UploadFile = form.get('imagem')
        autor_id: str = form.get('autor_id')
        texto: str = form.get('texto')

        nome_arquivo = self._upload_file(imagem=imagem,tipo='post')

        post: PostModel = PostModel(titulo=titulo, imagem=nome_arquivo,texto=texto,id_autor=autor_id)

        for id_tag in tags:
            tag = await self.get_tag(id_tag=int(id_tag))
            post.tags.append(tag)

        async with get_session() as session:
            session.add(post)
            await session.commit()
        

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            post: PostModel = await session.get(self.model,obj.id)

            if not post: return

            form = await self.request.form()

            titulo: str = form.get('titulo')
            texto: str = form.get('texto')
            autor_id: str = form.get('autor_id')
            imagem: UploadFile = form.get('imagem')
            tags: List[str] = form.getlist('tags')

            if titulo and titulo != post.titulo:
                post.titulo = titulo
            if tags:
                post.tags = []
                await session.commit()

                for id_tag in tags:
                    tag = await self.get_tag(id_tag = int(id_tag))
                    tag_local = await session.merge(tag)
                    post.tags.append(tag_local)

            if texto and texto != post.texto:
                post.texto =texto
            if autor_id and autor_id != post.id_autor:
                post.id_autor = autor_id
            if imagem.filename:
                novo_arquivo = await self._upload_file(imagem=imagem, tipo='post')
                post.imagem = novo_arquivo

            await session.commit()




    