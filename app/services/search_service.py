from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from app import models


def search_files(db: Session, query: str, tag_name: str = None) -> List[models.File]:
    q = db.query(models.File)

    if query:
        pattern = f"%{query}%"
        q = q.filter(
            or_(
                models.File.name.ilike(pattern),
                models.File.content.ilike(pattern),
            )
        )

    if tag_name:
        q = q.join(models.File.tags).filter(models.Tag.name == tag_name)

    return q.order_by(models.File.name).all()