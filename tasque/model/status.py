from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from .impl.database import Base
from .content import ContentEntity, ContentModel


class StatusEntity(Base):
    __tablename__ = "tsq_ticket_status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content_id = Column(Integer, ForeignKey("tsq_content.id"))

    content = relationship(ContentEntity)

    def to_model(self):
        return StatusModel(
            id=self.id, title=self.content.title, content=self.content.content
        )


class StatusModel(ContentModel):
    id: int
