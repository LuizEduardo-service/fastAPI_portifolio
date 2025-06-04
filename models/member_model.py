from sqlalchemy import Integer, Column, String
from controllers.core.base import Base
from sqlalchemy.orm import validates
from sqlalchemy.orm import Mapped, mapped_column


class MemberModel(Base):
    __tablename__ = 'membros'

    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    funcao: Mapped[str] = mapped_column(String(100))
    imagem: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(400))
    senha: Mapped[str] = mapped_column(String(400))

    @validates('funcao')
    def _valida_funcao(self, key, value):
        if value is None or value == '':
            raise ValueError('Informe uma função valida')
        if 'Python' not in value:
            raise ValueError('sua função deve Conter Python')
        
        return value
