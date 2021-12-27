from typing import Optional
from sqlalchemy import Column, Integer, Text
from .impl.database import Base
from pydantic import BaseModel


class ContentEntity(Base):
    __tablename__ = "tsq_content"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(Text, nullable=True)
    content = Column(Text, nullable=True)


class ContentModel(BaseModel):
    title: Optional[str]
    content: Optional[str]
