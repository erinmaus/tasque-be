from typing import List
from fastapi import HTTPException
from tasque.logging import get_logger
from tasque.model.content import ContentEntity
from tasque.model.ticket_to_ticket import TicketToTicketEntity
from tasque.model.project import ProjectEntity
from sqlalchemy.orm import Session
from ..model.ticket import (
    CreateTicketModel,
    TicketEntity,
    TicketModel,
    UpdateTicketModel,
)

logger = get_logger(__name__)


def create_ticket(db: Session, ticket: CreateTicketModel, project: ProjectEntity):
    content = ContentEntity(title=ticket.title, content=ticket.content)
    db.add(content)
    db.flush()

    result = TicketEntity(
        content_id=content.id,
        status_id=ticket.status_id,
        label_id=ticket.label_id,
        project_id=project.id,
        points=ticket.points,
    )
    db.add(result)
    db.flush()

    if ticket.parent_id:
        db.add(TicketToTicketEntity(parent_id=ticket.parent_id, child_id=result.id))
        db.flush()

    db.commit()

    return result


def get_ticket_by_id(db: Session, ticket_id: int, project: ProjectEntity):
    ticket = (
        db.query(TicketEntity)
        .filter(TicketEntity.id == ticket_id, TicketEntity.project_id == project.id)
        .first()
    )
    if ticket is None:
        logger.info(f"Could not find ticket '{ticket_id}' under project '{project.id}'")
        raise HTTPException(status_code=404, detail="Could not find ticket.")
    return ticket


def map_ticket_model_parents(db: Session, tickets: List[TicketModel]):
    ticket_ids = [t.id for t in tickets]

    parents = (
        db.query(TicketToTicketEntity)
        .filter(TicketToTicketEntity.child_id.in_(ticket_ids))
        .all()
    )

    index = {}
    for p in parents:
        index[p.child_id] = p.parent_id

    for t in tickets:
        parent_id = index.get(t.id, None)
        if not parent_id is None:
            t.parent_id = parent_id

    return index


def get_ticket_parent_id(db: Session, ticket: TicketEntity, project: ProjectEntity):
    ticket_to_ticket = (
        db.query(TicketToTicketEntity)
        .filter(TicketToTicketEntity.child_id == ticket.id)
        .first()
    )
    if ticket_to_ticket is None:
        return None

    return ticket_to_ticket.parent_id


def update_ticket(
    db: Session, ticket_id: int, ticket: UpdateTicketModel, project: ProjectEntity
):
    current_ticket = get_ticket_by_id(db, ticket_id, project)

    current_ticket.content.title = ticket.title or current_ticket.content.title
    current_ticket.content.content = ticket.content or current_ticket.content.content
    db.add(current_ticket.content)

    current_ticket.label_id = ticket.label_id or current_ticket.label_id
    current_ticket.status_id = ticket.status_id or current_ticket.status_id

    if not ticket.points is None:
        current_ticket.points = ticket.points

    db.add(current_ticket)

    current_parent_id = get_ticket_parent_id(db, current_ticket, project)
    if ticket.parent_id and ticket.parent_id != current_parent_id:
        logger.debug(f"Updating ticket {ticket_id} parent to {ticket.parent_id} (previously: {current_parent_id})")
        db.add(TicketToTicketEntity(parent_id=ticket.parent_id, child_id=ticket_id))

    db.commit()

    return current_ticket
