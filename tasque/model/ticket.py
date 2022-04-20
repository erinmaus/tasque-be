from datetime import date
from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer, Date, func
from sqlalchemy.orm import relationship
from .impl.database import Base
from .content import ContentModel


class TicketEntity(Base):
    __tablename__ = "tsq_ticket"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content_id = Column(Integer, ForeignKey("tsq_content.id"))
    status_id = Column(Integer, ForeignKey("tsq_ticket_status.id"))
    label_id = Column(Integer, ForeignKey("tsq_ticket_label.id"))
    project_id = Column(Integer, ForeignKey("tsq_project.id"))
    points = Column(Integer, nullable=False)
    status_update = Column(Date, server_default=func.sysdate())

    content = relationship("ContentEntity")
    status = relationship("StatusEntity")
    label = relationship("LabelEntity")
    project = relationship("ProjectEntity")

    def to_model(self):
        return TicketModel(
            id=self.id,
            title=self.content.title,
            content=self.content.content,
            status_id=self.status_id,
            label_id=self.label_id,
            project_id=self.project_id,
            points=self.points,
            status_update=self.status_update,
        )


class TicketModel(ContentModel):
    id: Optional[int]
    status_id: int
    label_id: int
    project_id: int
    points: int
    parent_id: Optional[int]
    status_update: date


class CreateTicketModel(ContentModel):
    status_id: int
    label_id: int
    points: int
    parent_id: Optional[int]


class UpdateTicketModel(ContentModel):
    status_id: Optional[int]
    label_id: Optional[int]
    points: Optional[int]
    parent_id: Optional[int]
