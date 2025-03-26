from sqlalchemy import Integer, Column, String
from controllers.core.base import Base
from sqlalchemy.orm import validates


class MemberModel(Base):
    __tablename__ = 'membros'

    id: str = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    funcao: str = Column(String(100))
    imagem: str = Column(String(100))


    @validates('funcao')
    def _valida_funcao(self, key, value):
        if value is None or value == '':
            raise ValueError('Informe uma função valida')
        if 'Python' not in value:
            raise ValueError('sua função deve envolvert python')
        
        return value
