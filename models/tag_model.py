from sqlalchemy import Column, Integer, String
from controllers.core.base import Base


class TagModel(Base):
    __tablename__: str = 'tags'


    id: int = Column(Integer, autoincrement=True, primary_key=True)
    tags: str = Column(String(100))
