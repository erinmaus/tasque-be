from typing import List
from tasque.model import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from tasque.controller.status import get_all_statuses
from tasque.model.account import AccountEntity
from tasque.model.status import StatusModel
from tasque.view.authentication import get_current_account

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/", response_model=List[StatusModel])
def index(
    db: Session = Depends(get_db),
    _current_user: AccountEntity = Depends(get_current_account),
):
    return [s.to_model() for s in get_all_statuses(db)]
