from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
import sqlalchemy.orm as orm
from controllers.core.base import Base


from sqlalchemy.orm import Mapped, mapped_column
from models.post_model import PostModel

from datetime import datetime

class ComentarioModel(Base):
    __tablename__: str = 'comentarios'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    id_post: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    post: Mapped[PostModel] = orm.relationship('PostModel', lazy='joined')
    autor: Mapped[str] = mapped_column(String(200))
    texto: Mapped[str] = mapped_column(String(200))