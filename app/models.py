from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Table
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


file_tags = Table(
    "file_tags",
    Base.metadata,
    Column("file_id", Integer, ForeignKey("files.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    parent = relationship("Folder", remote_side=[id], backref="children")
    files = relationship("File", back_populates="folder", cascade="all, delete")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_type = Column(String, default="note")
    content = Column(Text, nullable=True)
    file_path = Column(String, nullable=True)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    folder = relationship("Folder", back_populates="files")
    tags = relationship("Tag", secondary=file_tags, back_populates="files")
    review_item = relationship(
        "ReviewItem", back_populates="file",
        uselist=False, cascade="all, delete",
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    files = relationship("File", secondary=file_tags, back_populates="tags")


class ReviewItem(Base):
    __tablename__ = "review_items"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), unique=True, nullable=False)
    next_review_date = Column(DateTime, default=datetime.utcnow)
    interval = Column(Integer, default=1)
    ease_factor = Column(Integer, default=250)
    repetitions = Column(Integer, default=0)

    file = relationship("File", back_populates="review_item")