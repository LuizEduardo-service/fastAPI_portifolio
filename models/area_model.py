from sqlalchemy import Column, Integer, String
from controllers.core.base import Base


class AreaModel(Base):
    __tablename__: str = 'areas'

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    area: str = Column(String(100))