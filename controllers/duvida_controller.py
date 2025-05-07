from typing import List, Optional
from fastapi.requests import Request
from sqlalchemy.future import select


from controllers.core.configs import settings
from controllers.core.database import get_session
from models.duvida_model import DuvidaModel
from models.area_model import AreaModel
from controllers.base_controller import BaseController



class DuvidaController(BaseController):
    def __init__(self, request: Request):
        super().__init__(request, DuvidaModel)

    async def post_crud(self):
        form = await self.request.form()

        area_id: int = form.get('area')
        titulo: str = form.get('titulo')
        resposta: str = form.get('resposta')

        duvida: DuvidaModel = DuvidaModel(id_area=int(area_id), titulo=titulo, resposta=resposta)

        async with get_session() as session:
            session.add(duvida)
            await session.commit()


    async def put_crud(self, obj: object):
        async with get_session() as session:
            duvida: DuvidaModel = await session.get(DuvidaModel, obj.id)

            if duvida:
                form = self.request.form()
                area_id: int = form.get('area')
                titulo: str = form.get('titulo')
                resposta: str = form.get('resposta')

                if area_id and int(area_id) != duvida.id_area:
                    duvida.id_area = int(area_id)
                if titulo and titulo != duvida.titulo:
                    duvida.titulo = titulo
                if resposta and resposta != duvida.resposta:
                    duvida.resposta = resposta

                await session.commit()
        return await super().put_crud(obj)

    @property
    async def get_areas(self):
        async with get_session() as session:
            query = select(AreaModel)
            result = await session.execute(query)
            areas: Optional[List[AreaModel]] = result.scalars().all()
            return areas