from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List
from app import models


def create_review_item(db: Session, file_id: int) -> models.ReviewItem:
    existing = db.query(models.ReviewItem).filter(
        models.ReviewItem.file_id == file_id
    ).first()
    if existing:
        return existing

    item = models.ReviewItem(
        file_id=file_id,
        next_review_date=datetime.utcnow(),
        interval=1,
        ease_factor=250,
        repetitions=0,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_due_items(db: Session) -> List[models.ReviewItem]:
    now = datetime.utcnow()
    return db.query(models.ReviewItem).filter(
        models.ReviewItem.next_review_date <= now
    ).order_by(models.ReviewItem.next_review_date).all()


def answer_review_item(db: Session, item_id: int, quality: int) -> models.ReviewItem:
    if not 0 <= quality <= 5:
        raise ValueError("quality должен быть от 0 до 5")

    item = db.query(models.ReviewItem).get(item_id)
    if not item:
        raise ValueError(f"Карточка id={item_id} не найдена")

    if quality >= 3:
        if item.repetitions == 0:
            item.interval = 1
        elif item.repetitions == 1:
            item.interval = 6
        else:
            item.interval = int(round(item.interval * (item.ease_factor / 100)))
        item.repetitions += 1
    else:
        item.repetitions = 0
        item.interval = 1

    item.ease_factor = max(130, item.ease_factor + (quality - 3) * 10)

    item.next_review_date = datetime.utcnow() + timedelta(days=item.interval)
    db.commit()
    db.refresh(item)
    return item


def delete_review_item(db: Session, item_id: int) -> None:
    item = db.query(models.ReviewItem).get(item_id)
    if not item:
        raise ValueError(f"Карточка id={item_id} не найдена")
    db.delete(item)
    db.commit()