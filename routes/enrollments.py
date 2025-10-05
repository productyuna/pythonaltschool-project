from fastapi import APIRouter, status
from typing import List

from schemas.enrollment import Enrollment, EnrollmentCreate, EnrollmentUpdate
from services.enrollments import EnrollmentService

router = APIRouter()


@router.get("/", response_model=List[Enrollment])
def list_enrollments():
    return EnrollmentService.list_enrollments()


@router.get("/user/{user_id}", response_model=List[Enrollment])
def list_enrollments_for_user(user_id: int):
    return EnrollmentService.list_enrollments_for_user(user_id)


@router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
def enroll_user(payload: EnrollmentCreate):
    return EnrollmentService.enroll_user(payload.model_dump())


@router.post("/{enrollment_id}/complete", response_model=Enrollment)
@router.post("/{enrollment_id}/completion", response_model=Enrollment)
@router.put("/{enrollment_id}", response_model=Enrollment)
def mark_completion(enrollment_id: int, payload: EnrollmentUpdate):
    completed = payload.completed if payload.completed is not None else True
    return EnrollmentService.mark_completion(enrollment_id, completed)
