from typing import List
from tasque.model import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from tasque.controller.label import get_all_labels
from tasque.model.account import AccountEntity
from tasque.model.label import LabelModel
from tasque.view.authentication import get_current_account

router = APIRouter(prefix="/label", tags=["label"])


@router.get("/", response_model=List[LabelModel])
def index(
    db: Session = Depends(get_db),
    _current_user: AccountEntity = Depends(get_current_account),
):
    return [l.to_model() for l in get_all_labels(db)]
