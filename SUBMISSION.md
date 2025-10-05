### EduTrack Lite API

A lightweight FastAPI service to manage users, courses, and enrollments with in-memory storage and Pydantic validation.

- **Tech**: FastAPI, Pydantic v2, Starlette, httpx, pytest
- **Persistence**: In-memory lists/dicts (resets on process restart)
- **Auth**: None

### Project Layout
- `main.py`: FastAPI app bootstrap and router includes
- `routes/`: API route handlers
  - `routes/users.py`
  - `routes/courses.py`
  - `routes/enrollments.py`
- `services/`: In-memory services and business rules
  - `services/db.py` (stores and ID counters)
  - `services/users.py`
  - `services/courses.py`
  - `services/enrollments.py`
- `schemas/`: Pydantic models
  - `schemas/user.py`
  - `schemas/course.py`
  - `schemas/enrollment.py`
- `tests/`: Endpoint tests with TestClient
  - `tests/test_api.py`
- `requirements.txt`: Python dependencies

### Install & Run
Requirements: Python 3.10+

```bash
# from repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run tests
python3 -m pytest -q

# run server
uvicorn main:app --reload
# Docs: http://127.0.0.1:8000/docs
```

### Entities
- **User**: `{ id, name, email, is_active }` (default `is_active=true`)
- **Course**: `{ id, title, description, is_open }` (default `is_open=true`)
- **Enrollment**: `{ id, user_id, course_id, enrolled_date, completed }` (default `completed=false`)

### API Endpoints
- **Users**
  - `GET /users/`: List users
  - `POST /users/`: Create user (201)
  - `GET /users/{id}`: Get user
  - `PUT /users/{id}`: Update user (partial accepted)
  - `DELETE /users/{id}`: Delete user (204)
  - `POST /users/{id}/deactivate`: Set `is_active=false`

- **Courses**
  - `GET /courses/`: List courses
  - `POST /courses/`: Create course (201)
  - `GET /courses/{id}`: Get course
  - `PUT /courses/{id}`: Update course
  - `DELETE /courses/{id}`: Delete course (204)
  - `POST /courses/{id}/close`: Set `is_open=false`
  - `GET /courses/{id}/users`: List users enrolled in the course

- **Enrollments**
  - `GET /enrollments/`: List all enrollments
  - `GET /enrollments/user/{user_id}`: List enrollments for a user
  - `POST /enrollments/`: Enroll user in course (201)
  - `POST /enrollments/{id}/complete`: Mark completion (body `{ "completed": true|false }`; default true if omitted)
  - Also supported: `POST /enrollments/{id}/completion` and `PUT /enrollments/{id}` for marking completion

### Business Rules & Status Codes
- **Only active users can enroll**: 400 if inactive
- **Course must be open**: 400 if closed
- **No duplicate enrollment**: 409 if already enrolled
- **Missing resources**: 404 for user/course/enrollment not found
- **Create/Delete**: 201 on create, 204 on delete

### Example Payloads
- User: `{ "name": "Alice", "email": "alice@example.com", "is_active": true }`
- Course: `{ "title": "Python Basics", "description": "Learn Python", "is_open": true }`
- Enrollment: `{ "user_id": 1, "course_id": 1, "enrolled_date": "2025-09-16" }`

### Tests
- Location: `tests/test_api.py`
- Run: `python3 -m pytest -q`
- Coverage: CRUD for users/courses, deactivate user, close course, list course users, enroll with rules, mark completion, list enrollments.

### Notes
- Data resets on server restart (no DB). For persistence, replace `services/db.py` with a real datastore.
- `EmailStr` requires `email-validator` (already included).
