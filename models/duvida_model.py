from sqlalchemy import Column, Integer, ForeignKey, String
from controllers.core.base import Base
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column
from models.area_model import AreaModel


class DuvidaModel(Base):
    __tablename__: str = 'duvida'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    id_area: Mapped[int] = mapped_column(Integer, ForeignKey('areas.id'))
    area: Mapped[AreaModel] = orm.relationship('AreaModel', lazy='joined')
    titulo: Mapped[str] = mapped_column(String(200))
    resposta: Mapped[str] = mapped_column(String(400))