from fastapi.requests import Request
from fastapi import UploadFile

from controllers.core.database import get_session
from models.member_model import MemberModel
from controllers.base_controller import BaseController
from controllers.core.auth import verificar_senha, gerar_hash_senha
from sqlalchemy.future import select

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
        hash_senha: str = gerar_hash_senha(senha=senha)


        novo_nome: str = await self._upload_file(imagem=imagem, tipo='membro')
        membro: MemberModel = MemberModel(nome=nome, funcao=funcao, imagem = novo_nome, email = email, senha= hash_senha)

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
                hash_senha: str = gerar_hash_senha(senha=senha)

                if nome and membro.nome != nome:
                    membro.nome = nome
                if funcao and membro.funcao != funcao:
                    membro.funcao = funcao
                if email and membro.email != email:
                    membro.email = email
                if senha and membro.senha != hash_senha:
                    membro.senha = hash_senha 
                
                if imagem.filename:
                    novo_nome: str = await self._upload_file(imagem=imagem, tipo='membro')
                    membro.imagem = novo_nome

                await session.commit()

    async def login_membro(self, email: str, senha: str):
        async with get_session() as session:
            query = select(MemberModel).filter(MemberModel.email == email)
            result = await session.execute(query)

            membro = result.scalar_one_or_none()

            if not membro:
                return None
            
            if not verificar_senha(senha=senha, hash_senha=membro.senha):
                return None
            
            return membro
