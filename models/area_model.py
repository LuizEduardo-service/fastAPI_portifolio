from sqlalchemy import Column, Integer, String
from controllers.core.base import Base
from sqlalchemy.orm import Mapped ,mapped_column


class AreaModel(Base):
    __tablename__: str = 'areas'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    area: Mapped[str] = mapped_column(String(100))