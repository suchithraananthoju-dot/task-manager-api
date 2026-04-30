# Task Manager API

A backend Task Management REST API built using FastAPI and SQLite.

## Features

- Create Tasks
- Get All Tasks
- Update Tasks
- Delete Tasks
- SQLite Database Integration
- RESTful APIs
- Error Handling

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## Project Structure

task_manager_api/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── requirements.txt
├── README.md
├── .gitignore

## Installation

1. Clone Repository

git clone <your-github-repo-link>

2. Navigate to project folder

cd task_manager_api

3. Create Virtual Environment

python -m venv venv

4. Activate Environment

Windows:
venv\Scripts\activate

5. Install Dependencies

pip install -r requirements.txt

6. Run Server

uvicorn main:app --reload

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | Get all tasks |
| POST | /tasks | Create task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |

## Future Enhancements

- User Authentication
- JWT Token Security
- Task Filtering
- Deployment on Cloud

## Author

Ananthoju Suchithra