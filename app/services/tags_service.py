from sqlalchemy.orm import Session
from typing import List
from app import models


def create_tag(db: Session, name: str) -> models.Tag:
    existing = db.query(models.Tag).filter(models.Tag.name == name).first()
    if existing:
        return existing
    tag = models.Tag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def list_tags(db: Session) -> List[models.Tag]:
    return db.query(models.Tag).order_by(models.Tag.name).all()


def delete_tag(db: Session, tag_id: int) -> None:
    tag = db.query(models.Tag).get(tag_id)
    if not tag:
        raise ValueError(f"Тег id={tag_id} не найден")
    db.delete(tag)
    db.commit()


def attach_tag_to_file(db: Session, file_id: int, tag_id: int) -> models.File:
    file = db.query(models.File).get(file_id)
    if not file:
        raise ValueError(f"Файл id={file_id} не найден")
    tag = db.query(models.Tag).get(tag_id)
    if not tag:
        raise ValueError(f"Тег id={tag_id} не найден")
    if tag not in file.tags:
        file.tags.append(tag)
        db.commit()
        db.refresh(file)
    return file


def detach_tag_from_file(db: Session, file_id: int, tag_id: int) -> models.File:
    file = db.query(models.File).get(file_id)
    if not file:
        raise ValueError(f"Файл id={file_id} не найден")
    tag = db.query(models.Tag).get(tag_id)
    if tag and tag in file.tags:
        file.tags.remove(tag)
        db.commit()
        db.refresh(file)
    return file