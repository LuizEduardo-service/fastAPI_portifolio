from typing import Optional, List
from fastapi.requests import Request
from sqlalchemy.future import select

from controllers.core.database import get_session


class BaseController:

    def __init__(self, request: Request, model: object):
        self.request: Request = request
        self.model: object = model

    async def get_all(self) -> Optional[List[object]]:
        """retorna uma lista de objetos"""
        async with get_session() as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars().all()
        
    async def get_one_crud(self, id_obj: int) -> Optional[object]:
        """retorna um objeot com base no id"""

        async with get_session() as session:
            obj = await session.get(self.model, id_obj)

            return obj
        
    async def delete_crud(self, id_obj: int) -> None:
        """deleta um objeto """

        async with get_session() as session:
            obj = await session.get(self.model, id_obj)

            if obj:
                await session.delete(obj)
                await session.commit()

    async def post_crud(self) -> None:
        raise NotImplementedError('Metodo não implementado')
    
    async def put_crud(self, obj: object) -> None:
        raise NotImplementedError("Metodo não implementado")
        
    