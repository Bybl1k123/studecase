from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class FolderCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    parent_id: Optional[int] = None


class FolderOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class NoteCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    content: str = ""
    folder_id: Optional[int] = None


class FileOut(BaseModel):
    id: int
    name: str
    file_type: str
    content: Optional[str]
    file_path: Optional[str]
    folder_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class TagOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ReviewOut(BaseModel):
    id: int
    file_id: int
    next_review_date: datetime
    interval: int
    repetitions: int

    class Config:
        from_attributes = True