from pydantic import BaseModel, Field
from typing import Optional


class CourseBase(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    is_open: bool = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    is_open: Optional[bool] = None


class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True
