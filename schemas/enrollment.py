from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int
    enrolled_date: date
    completed: bool = False


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    completed: Optional[bool] = None


class Enrollment(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True
