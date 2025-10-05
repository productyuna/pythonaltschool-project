from fastapi import FastAPI

from routes.users import router as users_router
from routes.courses import router as courses_router
from routes.enrollments import router as enrollments_router

app = FastAPI(title="EduTrack Lite API")

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(courses_router, prefix="/courses", tags=["courses"])
app.include_router(enrollments_router, prefix="/enrollments", tags=["enrollments"])


@app.get("/")
def root():
    return {"message": "EduTrack Lite API"}
