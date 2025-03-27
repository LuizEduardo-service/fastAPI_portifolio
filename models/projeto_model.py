from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from controllers.core.base import Base
from sqlalchemy.orm import mapped_column, Mapped


class ProjetoModel(Base):
    __tablename__: str = 'projetos'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    titulo: Mapped[str] = mapped_column(String(100))
    descricao_inicial: Mapped[str] = mapped_column(String(300))
    imagem1: Mapped[str] = mapped_column(String(100))
    imagem2: Mapped[str] = mapped_column(String(100))
    imagem3: Mapped[str] = mapped_column(String(100))
    descricao_final: Mapped[str]  =mapped_column(String(300))
    link: Mapped[str] = mapped_column(String(200))