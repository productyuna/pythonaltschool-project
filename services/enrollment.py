from typing import List
from fastapi import HTTPException, status

from services.db import enrollments, users, courses, next_id


class EnrollmentService:
    @staticmethod
    def list_enrollments() -> List[dict]:
        return enrollments

    @staticmethod
    def list_enrollments_for_user(user_id: int) -> List[dict]:
        return [e for e in enrollments if e["user_id"] == user_id]

    @staticmethod
    def list_users_for_course(course_id: int) -> List[dict]:
        user_ids = [e["user_id"] for e in enrollments if e["course_id"] == course_id]
        return [u for u in users if u["id"] in user_ids]

    @staticmethod
    def enroll_user(data: dict) -> dict:
        user = next((u for u in users if u["id"] == data["user_id"]), None)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not user.get("is_active", True):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active")

        course = next((c for c in courses if c["id"] == data["course_id"]), None)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        if not course.get("is_open", True):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course is not open for enrollment")

        existing = next((e for e in enrollments if e["user_id"] == data["user_id"] and e["course_id"] == data["course_id"]), None)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already enrolled in this course")

        new_enrollment = {"id": next_id("enrollment"), **data}
        enrollments.append(new_enrollment)
        return new_enrollment

    @staticmethod
    def mark_completion(enrollment_id: int, completed: bool) -> dict:
        enrollment = next((e for e in enrollments if e["id"] == enrollment_id), None)
        if not enrollment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
        enrollment["completed"] = completed
        return enrollment
