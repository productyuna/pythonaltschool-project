from typing import List
from fastapi import HTTPException, status

from services.db import courses, next_id


class CourseService:
    @staticmethod
    def list_courses() -> List[dict]:
        return courses

    @staticmethod
    def get_course(course_id: int) -> dict:
        course = next((c for c in courses if c["id"] == course_id), None)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        return course

    @staticmethod
    def create_course(data: dict) -> dict:
        new_course = {"id": next_id("course"), **data}
        courses.append(new_course)
        return new_course

    @staticmethod
    def update_course(course_id: int, data: dict) -> dict:
        course = CourseService.get_course(course_id)
        course.update({k: v for k, v in data.items() if v is not None})
        return course

    @staticmethod
    def delete_course(course_id: int) -> None:
        course = CourseService.get_course(course_id)
        courses.remove(course)

    @staticmethod
    def close_enrollment(course_id: int) -> dict:
        course = CourseService.get_course(course_id)
        course["is_open"] = False
        return course
