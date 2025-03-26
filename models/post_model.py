from datetime import datetime
from sqlalchemy import Column, Integer, String, Table, DateTime, ForeignKey
from controllers.core.base import Base
from typing import List

from models.tag_model import TagModel
from models.autor_model import AutorModel

import sqlalchemy.orm as orm


tags_post = Table(
    'tags_post',
    Base.metadata,
    Column('id_post', Integer, ForeignKey('posts.id')),
    Column('id_tags', Integer, ForeignKey('tags.id'))
)

comentarios_post = Table(
    'comentarios_post',
    Base.metadata,
    Column('id_post', Integer, ForeignKey('posts.id')),
    Column('id_comentario', Integer, ForeignKey('comentarios.id'))
)

class PostModel(Base):
    __tablename__: str = 'posts'

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    titulo: str = Column(String(200))
    data: datetime = Column(DateTime, default=datetime.now, index=True)

    tags: List[TagModel] = orm.relationship('TagModel', secondary=tags_post, backref='tagp', lazy='joined')

    imagem: str = Column(String(200))
    text: str  = Column(String(200))

    comentarios: List[object] = orm.relationship('ComentarioModel', secondary=comentarios_post, backref='comentario', lazy='joined')

    id_autor: int = Column(Integer, ForeignKey('autores.id'))
    autor: AutorModel = orm.relationship('AutorModel', lazy='joined')