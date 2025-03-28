from fastapi.requests import Request
from fastapi import UploadFile

from aiofile import async_open

from uuid import uuid4

from controllers.core.configs import settings
from controllers.core.database import get_session
from models.member_model import MemberModel
from controllers.base_controller import BaseController

class MembroController(BaseController):

    def __init__(self, request, model):
        super().__init__(request, MemberModel)


    async def post_crud(self) -> None:
        form = self.request.form()

        nome: str = form.get('nome')
        funcao: str = form.get('funcao')
        imagem: UploadFile = form.get('image')


        novo_nome: str = upload_file(imagem=imagem)
        membro: MemberModel = MemberModel(nome=nome, funcao=funcao, imagem = novo_nome)

        async with get_session() as session:
            session.add(membro)
            await session.commit()
    
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            membro: MemberModel = await session.get(MemberModel, obj.id)

            if membro:
                form = self.request.form()
                nome: str = form.get('nome')
                funcao: str = form.get('funcao')
                imagem: UploadFile = form.get(imagem)

                if membro.nome and membro.nome != nome:
                    membro.nome = nome
                if membro.funcao and membro.funcao != funcao:
                    membro.funcao = funcao
                
                if imagem.filename:
                    novo_nome: str = upload_file(imagem=imagem)
                    membro.imagem = novo_nome

async def upload_file(imagem: UploadFile) -> str:
    """realiza o upload e retona o novo nome do arquivo"""

    try:
        ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f'{str(uuid4())}.{ext}'                   
        async with async_open(f'{settings.MEDIA}/{novo_nome}') as file:
            await file.write(imagem.read())

        return novo_nome
    except Exception as e:
        raise Exception('Erro ao salvar imagem')
