from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .impl.database import Base


class AccountEntity(Base):
    __tablename__ = "tsq_account"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(16), nullable=False, unique=True)
    email = Column(String(254), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    organization_id = Column(Integer, ForeignKey("tsq_organization.id"))

    organization = relationship("OrganizationEntity")

    def to_model(self):
        return AccountModel(
            id=self.id,
            username=self.username,
            email=self.email,
            organization_id=self.organization_id,
        )


class AccountModel(BaseModel):
    id: int
    username: str
    email: str
    organization_id: int
