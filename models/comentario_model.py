from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
import sqlalchemy.orm as orm
from controllers.core.base import Base

from models.post_model import PostModel

from datetime import datetime

class ComentarioModel(Base):
    __tablename__: str = 'comentarios'

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    data: datetime = Column(DateTime, default=datetime.now, index=True)

    id_post: int = Column(Integer, ForeignKey('posts.id'))
    post: PostModel = orm.relationship('PostModel', lazy='joined')

    autor: str = Column(String(200))
    texto: str = Column(String(200))