from fastapi.requests import Request

from controllers.core.database import get_session
from models.comentario_model import ComentarioModel
from controllers.base_controller import BaseController


class ComentarioController(BaseController):
    def __init__(self, request: Request):
        super().__init__(request, ComentarioModel)

    async def post_crud(self):

        form = await self.request.form()

        post_id:int = form.get('post')
        autor: str = form.get('autor')
        texto: str = form.get('texto')

        comentario: ComentarioModel = ComentarioModel(id_post= int(post_id), autor= autor, texto=texto)

        async with get_session() as session:
            session.add(comentario)
            await session.commit()

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            comentario:ComentarioModel = await session.get(self.model, obj.id)

            if comentario:
                form = await self.request.form()

                post_id: int = form.get('post')
                autor: str = form.get('autor')
                texto: str = form.get('texto')

                if post_id and int(post_id) != comentario.id_post:
                    comentario.id_post = int(post_id)

                if autor and autor != comentario.autor:
                    comentario.autor = autor

                if texto and texto != comentario.texto:
                    comentario.texto = texto

                await session.commit()



        return await super().put_crud(obj)

    