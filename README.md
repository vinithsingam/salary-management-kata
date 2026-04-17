# Salary Management API

## Features
- CRUD Employees
- Salary calculation (India 10%, USA 12%)
- Metrics APIs

## Tech Stack
- FastAPI
- SQLAlchemy
- Pytest

## How to Run
pip install -r requirements.txt
uvicorn app.main:app --reload

## Run Tests
pytest

## API Endpoints
- POST /employees
- GET /employees
- GET /employees/{id}
- PUT /employees/{id}
- DELETE /employees/{id}
- GET /employees/{id}/salary
- GET /metrics/country/{country}
- GET /metrics/job-title/{job_title}

## AI Usage
Used ChatGPT for:
- Fixing data model issues
- Implementing salary logic
- Writing tests with pytest fixtures
- Debugging import and test issues