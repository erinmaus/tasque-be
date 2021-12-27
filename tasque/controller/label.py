from tasque.model.label import LabelEntity
from sqlalchemy.orm import Session


def get_all_labels(db: Session):
    return db.query(LabelEntity).all()
