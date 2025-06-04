from fastapi.requests import Request
from fastapi import UploadFile

from controllers.core.database import get_session
from models.member_model import MemberModel
from controllers.base_controller import BaseController

class MembroController(BaseController):

    def __init__(self, request: Request):
        super().__init__(request, MemberModel)


    async def post_crud(self) -> None:
        form =  await self.request.form()

        nome: str = form.get('nome')
        funcao: str = form.get('funcao')
        imagem: UploadFile = form.get('imagem')
        email: str = form.get('email')
        senha: str = form.get('senha')# TODO: ADICIONAR HASH


        novo_nome: str = await self._upload_file(imagem=imagem, tipo='membro')
        membro: MemberModel = MemberModel(nome=nome, funcao=funcao, imagem = novo_nome, email = email, senha= senha)

        async with get_session() as session:
            session.add(membro)
            await session.commit()
    
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            membro: MemberModel = await session.get(MemberModel, obj.id)

            if membro:
                form = await self.request.form()
                nome: str = form.get('nome')
                funcao: str = form.get('funcao')
                imagem: UploadFile = form.get('imagem')
                email: str = form.get('email')
                senha: str = form.get('senha')

                if membro.nome and membro.nome != nome:
                    membro.nome = nome
                if membro.funcao and membro.funcao != funcao:
                    membro.funcao = funcao
                if membro.email and membro.email != email:
                    membro.email = email
                if membro.senha and membro.senha != senha:
                    membro.senha = senha #TODO: ADICIONAR HASH
                
                if imagem.filename:
                    novo_nome: str = await self._upload_file(imagem=imagem, tipo='membro')
                    membro.imagem = novo_nome

                await session.commit()


