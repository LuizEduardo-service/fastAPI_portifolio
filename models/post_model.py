from datetime import datetime
from sqlalchemy import Column, Integer, String, Table, DateTime, ForeignKey
from controllers.core.base import Base
from typing import List

from models.tag_model import TagModel
from models.autor_model import AutorModel
from sqlalchemy.orm import Mapped, mapped_column

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

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    tags: Mapped[List[TagModel]] = orm.relationship('TagModel', secondary=tags_post, backref='tagp', lazy='joined')
    imagem: Mapped[str] = mapped_column(String(200))
    texto: Mapped[str]  = mapped_column(String(200))
    comentarios: Mapped[List[object]] = orm.relationship('ComentarioModel', secondary=comentarios_post, backref='comentario', lazy='joined')
    id_autor: Mapped[int] = mapped_column(Integer, ForeignKey('autores.id'))
    autor: Mapped[AutorModel] = orm.relationship('AutorModel', lazy='joined')