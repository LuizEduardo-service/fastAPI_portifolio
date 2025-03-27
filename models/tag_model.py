from sqlalchemy import Column, Integer, String
from controllers.core.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class TagModel(Base):
    __tablename__: str = 'tags'


    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    tags: Mapped[str] = mapped_column(String(100))
