from fastapi import APIRouter, status
from typing import List

from schemas.course import Course, CourseCreate, CourseUpdate
from schemas.user import User
from services.courses import CourseService
from services.enrollments import EnrollmentService

router = APIRouter()


@router.get("/", response_model=List[Course])
def list_courses():
    return CourseService.list_courses()


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    return CourseService.get_course(course_id)


@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate):
    return CourseService.create_course(payload.model_dump())


@router.put("/{course_id}", response_model=Course)
def update_course(course_id: int, payload: CourseUpdate):
    return CourseService.update_course(course_id, payload.model_dump())


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    CourseService.delete_course(course_id)
    return None


@router.post("/{course_id}/close", response_model=Course)
def close_enrollment(course_id: int):
    return CourseService.close_enrollment(course_id)


@router.get("/{course_id}/users", response_model=List[User])
def list_users_enrolled(course_id: int):
    return EnrollmentService.list_users_for_course(course_id)
