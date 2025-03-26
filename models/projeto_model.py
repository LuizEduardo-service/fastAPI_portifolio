from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from controllers.core.base import Base


class ProjetoModel(Base):
    __tablename__: str = 'projetos'

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    data: datetime = Column(DateTime, default=datetime.now, index=True)
    titulo: str = Column(String(100))
    descricao_inicial: str = Column(String(300))
    imagem1: str = Column(String(100))
    imagem2: str = Column(String(100))
    imagem3: str = Column(String(100))
    descricao_final: str  = Column(String(300))
    link: str = Column(String(200))