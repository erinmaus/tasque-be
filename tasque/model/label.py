from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from .impl.database import Base
from .content import ContentEntity, ContentModel


class LabelEntity(Base):
    __tablename__ = "tsq_ticket_label"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content_id = Column(Integer, ForeignKey("tsq_content.id"))

    content = relationship(ContentEntity)

    def to_model(self):
        return LabelModel(
            id=self.id, title=self.content.title, content=self.content.content
        )


class LabelModel(ContentModel):
    id: int
