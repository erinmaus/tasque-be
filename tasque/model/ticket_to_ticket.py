from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from .impl.database import Base


class TicketToTicketEntity(Base):
    __tablename__ = "tsq_ticket_parent"

    parent_id = Column(
        Integer, ForeignKey("tsq_project.id"), primary_key=True, index=True, unique=True
    )
    child_id = Column(
        Integer, ForeignKey("tsq_project.id"), primary_key=True, index=True, unique=True
    )
