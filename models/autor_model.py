from sqlalchemy import Column, Integer, String, ForeignKey, Table
from controllers.core.base import Base
import sqlalchemy.orm as orm
from typing import List
from models.tag_model import TagModel


tags_autor = Table(
    'tags_autor',
    Base.metadata,
    Column('id_autor', Integer, ForeignKey('autores.id')),
    Column('id_tag', Integer, ForeignKey('tags.id'))
)

class AutorModel(Base):
    __tablename__: str = 'autores'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    imagem: str = Column(String(100))

    tags: List[TagModel] = orm.relationship('TagModel', secondary=tags_autor, backref='taga', lazy='joined')  