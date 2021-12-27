from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from .impl.database import Base


class OrganizationEntity(Base):
    __tablename__ = "tsq_organization"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(Text, nullable=False)

    projects = relationship("ProjectEntity")

    def to_model(self):
        return OrganizationModel(
            id=self.id, title=self.title, project_ids=[p.id for p in self.projects]
        )


class OrganizationModel(BaseModel):
    id: int
    title: str
    project_ids: List[int]
