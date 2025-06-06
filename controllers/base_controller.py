# type: ignore
from typing import Optional, List
from fastapi import UploadFile
from fastapi.requests import Request
from sqlalchemy.future import select
from controllers.core.configs import settings
from uuid import uuid4
from aiofile import async_open

from controllers.core.database import get_session

from models.post_model import PostModel
from models.tag_model import TagModel
from models.autor_model import AutorModel


class BaseController:

    def __init__(self, request: Request, model: object):
        self.request: Request = request
        self.model: object = model

    async def get_all(self) -> Optional[List[object]]:
        """retorna uma lista de objetos"""
        async with get_session() as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars().unique().all()
        
    async def get_one_crud(self, id_obj: int) -> Optional[object]:
        """retorna um objeto com base no id"""

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
        
    async def _upload_file(self, imagem: UploadFile, tipo: str) -> str:
        """realiza o upload e retona o novo nome do arquivo"""

        try:
            ext: str = imagem.filename.split('.')[-1]
            novo_nome: str = f'{str(uuid4())}.{ext}'                   
            async with async_open(f'{settings.MEDIA}/{tipo}/{novo_nome}', "wb") as file:
                await file.write(imagem.file.read())

            return novo_nome
        except Exception as e:
            raise Exception(f'Erro ao salvar imagem: {e}')
           
    async def get_objetos(self, model_obj:object) -> Optional[List[object]]:
        async with get_session() as session:
            query = select(model_obj)
            result = await session.execute(query)
            objetos: Optional[List[model_obj]] = result.scalars().unique().all() 

        return objetos
    
    async def get_objeto(self, model_obj: object, id_obj: int) -> Optional[object]:
        async with get_session() as session:
            objeto: model_obj = await session.get(model_obj, id_obj)
            return objeto