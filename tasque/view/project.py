from tasque.model.project_ticket_query import ProjectTicketQuery
from tasque.controller.ticket import (
    create_ticket,
    get_ticket_by_id,
    get_ticket_parent_id,
    map_ticket_model_parents,
    update_ticket,
)
from tasque.model.ticket import CreateTicketModel, TicketModel, UpdateTicketModel
from typing import List
from tasque.model.project import ProjectModel
from tasque.model import get_db
from tasque.model.account import AccountEntity
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .authentication import get_current_account
from ..controller.project import (
    get_all_tickets_under_project,
    get_project_by_id,
    get_projects_under_org,
)

router = APIRouter(prefix="/project", tags=["project"])


@router.get("/", response_model=List[ProjectModel])
def index(
    db: Session = Depends(get_db),
    current_user: AccountEntity = Depends(get_current_account),
):
    return [p.to_model() for p in get_projects_under_org(db, current_user.organization)]


@router.get("/{id}", response_model=ProjectModel)
def get_project(
    id: int,
    db: Session = Depends(get_db),
    current_user: AccountEntity = Depends(get_current_account),
):
    return get_project_by_id(db, id, current_user.organization).to_model()


@router.get("/{id}/ticket", response_model=List[TicketModel])
def get_tickets_under_project(
    id: int,
    query: ProjectTicketQuery = Depends(),
    db: Session = Depends(get_db),
    current_user: AccountEntity = Depends(get_current_account),
):
    result = [
        t.to_model()
        for t in get_all_tickets_under_project(db, id, query, current_user.organization)
    ]

    map_ticket_model_parents(db, result)

    return result


@router.post("/{id}/ticket", response_model=TicketModel)
def create_ticket_under_project(
    id: int,
    ticket: CreateTicketModel,
    db: Session = Depends(get_db),
    current_user: AccountEntity = Depends(get_current_account),
):
    project = get_project_by_id(db, id, current_user.organization)
    result = create_ticket(db, ticket, project).to_model()
    result.parent_id = get_ticket_parent_id(db, ticket, project)
    return result


@router.patch("/{project_id}/ticket/{ticket_id}", response_model=TicketModel)
def update_ticket_under_project(
    project_id: int,
    ticket_id: int,
    ticket: UpdateTicketModel,
    db: Session = Depends(get_db),
    current_user: AccountEntity = Depends(get_current_account),
):
    project = get_project_by_id(db, project_id, current_user.organization)
    result = update_ticket(db, ticket_id, ticket, project).to_model()
    result.parent_id = get_ticket_parent_id(db, result, project)
    return result


@router.get("/{project_id}/ticket/{ticket_id}", response_model=TicketModel)
def get_ticket_under_project(
    project_id: int,
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: AccountEntity = Depends(get_current_account),
):
    project = get_project_by_id(db, project_id, current_user.organization)
    result = get_ticket_by_id(db, ticket_id, project).to_model()
    result.parent_id = get_ticket_parent_id(db, result, project)
    return result
