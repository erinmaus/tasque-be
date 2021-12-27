from tasque.model.status import StatusEntity
from sqlalchemy.orm import Session


def get_all_statuses(db: Session):
    return db.query(StatusEntity).all()
