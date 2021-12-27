from enum import Enum
from typing import Optional
from pydantic import BaseModel


class ProjectTicketQueryLookupType(str, Enum):
    orphans = "orphans"
    all = "all"


class ProjectTicketQuery(BaseModel):
    lookup_type: Optional[ProjectTicketQueryLookupType]
    label: Optional[int]
    status: Optional[int]
    offset: Optional[int]
    limit: Optional[int]
