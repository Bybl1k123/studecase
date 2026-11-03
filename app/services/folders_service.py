from sqlalchemy.orm import Session
from typing import List, Optional
from app import models
from app.schemas import FolderCreate


def create_folder(db: Session, data: FolderCreate) -> models.Folder:
    if data.parent_id is not None:
        parent = db.query(models.Folder).get(data.parent_id)
        if not parent:
            raise ValueError(f"Родительская папка id={data.parent_id} не найдена")

    folder = models.Folder(name=data.name, parent_id=data.parent_id)
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


def get_folder(db: Session, folder_id: int) -> Optional[models.Folder]:
    return db.query(models.Folder).get(folder_id)


def list_folders(db: Session, parent_id: Optional[int] = None) -> List[models.Folder]:
    query = db.query(models.Folder)
    if parent_id is None:
        query = query.filter(models.Folder.parent_id.is_(None))
    else:
        query = query.filter(models.Folder.parent_id == parent_id)
    return query.order_by(models.Folder.name).all()


def rename_folder(db: Session, folder_id: int, new_name: str) -> models.Folder:
    folder = db.query(models.Folder).get(folder_id)
    if not folder:
        raise ValueError(f"Папка id={folder_id} не найдена")
    folder.name = new_name
    db.commit()
    db.refresh(folder)
    return folder


def move_folder(db: Session, folder_id: int, new_parent_id: Optional[int]) -> models.Folder:
    folder = db.query(models.Folder).get(folder_id)
    if not folder:
        raise ValueError(f"Папка id={folder_id} не найдена")

    if new_parent_id is not None:
        if new_parent_id == folder_id:
            raise ValueError("Нельзя переместить папку в саму себя")
        parent = db.query(models.Folder).get(new_parent_id)
        if not parent:
            raise ValueError(f"Родитель id={new_parent_id} не найден")
        p = parent
        while p is not None:
            if p.id == folder_id:
                raise ValueError("Нельзя переместить папку в своего потомка")
            p = p.parent

    folder.parent_id = new_parent_id
    db.commit()
    db.refresh(folder)
    return folder


def delete_folder(db: Session, folder_id: int) -> None:
    folder = db.query(models.Folder).get(folder_id)
    if not folder:
        raise ValueError(f"Папка id={folder_id} не найдена")
    db.delete(folder)
    db.commit()


def get_folder_tree(db: Session, parent_id: Optional[int] = None) -> list:
    result = []
    for folder in list_folders(db, parent_id):
        result.append({
            "id": folder.id,
            "name": folder.name,
            "children": get_folder_tree(db, folder.id),
        })
    return result