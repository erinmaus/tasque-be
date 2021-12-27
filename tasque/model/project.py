from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, Text
from .impl.database import Base


class ProjectEntity(Base):
    __tablename__ = "tsq_project"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(Text, nullable=False)
    organization_id = Column(Integer, ForeignKey("tsq_organization.id"))

    def to_model(self):
        return ProjectModel(
            id=self.id, title=self.title, organization_id=self.organization_id
        )


class ProjectModel(BaseModel):
    id: int
    title: str
    organization_id: int
