from tasque.model.project_ticket_query import (
    ProjectTicketQuery,
    ProjectTicketQueryLookupType,
)
from tasque.model.ticket_to_ticket import TicketToTicketEntity
from tasque.logging import get_logger
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..model.organization import OrganizationEntity
from ..model.project import ProjectEntity
from ..model.ticket import TicketEntity

logger = get_logger(__name__)


def get_projects_under_org(db: Session, organization: OrganizationEntity):
    return (
        db.query(ProjectEntity)
        .filter(ProjectEntity.organization_id == organization.id)
        .all()
    )


def get_project_by_id(db: Session, project_id: int, organization: OrganizationEntity):
    project = (
        db.query(ProjectEntity)
        .filter(
            ProjectEntity.organization_id == organization.id,
            ProjectEntity.id == project_id,
        )
        .first()
    )
    if project is None:
        logger.info(
            f"Could not find project '{project_id}' under organization '{organization.id}'"
        )
        raise HTTPException(status_code=404, detail="Could not find project.")
    return project


def get_all_tickets_under_project(
    db: Session,
    project_id: int,
    query: ProjectTicketQuery,
    organization: OrganizationEntity,
):
    base_query = (
        db.query(TicketEntity)
        .join(ProjectEntity)
        .filter(
            TicketEntity.project_id == project_id,
            ProjectEntity.organization_id == organization.id,
        )
    )

    if (
        query.lookup_type is None
        or query.lookup_type == ProjectTicketQueryLookupType.orphans
    ):
        base_query = base_query.except_(
            db.query(TicketEntity).filter(
                TicketEntity.id == TicketToTicketEntity.child_id
            )
        )

    if not query.status is None:
        base_query = base_query.filter(TicketEntity.status_id == query.status)

    if not query.label is None:
        base_query = base_query.filter(TicketEntity.label_id == query.label)

    if not query.offset is None:
        base_query = base_query.offset(query.offset)

    if not query.limit is None:
        base_query = base_query.limit(query.limit)

    return base_query.all()
