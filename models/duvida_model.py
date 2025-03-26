from sqlalchemy import Column, Integer, ForeignKey, String
from controllers.core.base import Base
import sqlalchemy.orm as orm
from models.area_model import AreaModel


class DuvidaModel(Base):
    __tablename__: str = 'duvida'

    id: int = Column(Integer, autoincrement=True, primary_key=True)

    id_area: int = Column(Integer, ForeignKey('areas.id'))
    area: AreaModel = orm.relationship('AreaModel', lazy='joined')

    titulo: str = Column(String(200))
    resposta: str = Column(String(400))