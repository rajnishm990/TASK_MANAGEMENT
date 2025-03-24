# Task Management API

A Django-based RESTful API for managing tasks and users. This API allows you to create tasks, assign them to users, and retrieve tasks for specific users.

## Features

- Create, read, update, and delete tasks
- Assign tasks to multiple users
- Get all tasks assigned to a specific user
- API documentation with Swagger and ReDoc

## Requirements

- Python 
- Django 
- Django Rest Framework

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd task-management-project
```

### 2. Create a virtual environment and activate it

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

## API Documentation

API documentation is available at:
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## API Endpoints

### Tasks

- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Retrieve a specific task
- `PUT /api/tasks/{id}/` - Update a task
- `DELETE /api/tasks/{id}/` - Delete a task
- `POST /api/tasks/{id}/assign_users/` - Assign users to a task
- `DELETE /api/tasks/{id}/unassign_users/` - Remove task assignments

### Users

- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Retrieve a specific user
- `GET /api/users/{id}/tasks/` - Get tasks assigned to a specific user

## Sample API Requests and Responses

### Create a Task

**Request:**
```http
POST /api/tasks/
Content-Type: application/json

{
  "name": "Implement login feature",
  "description": "Create login page with authentication",
  "task_type": "FEATURE",
  "status": "PENDING"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Implement login feature",
  "description": "Create login page with authentication",
  "created_at": "2023-10-25T14:30:45.123456Z",
  "task_type": "FEATURE",
  "completed_at": null,
  "status": "PENDING",
  "assigned_users": []
}
```

### Assign Users to a Task

**Request:**
```http
POST /api/tasks/1/assign_users/
Content-Type: application/json

{
  "user_ids": [1, 2]
}
```

**Response:**
```json
[
  {
    "task": 1,
    "user": 1,
    "assigned_at": "2023-10-25T14:35:12.123456Z"
  },
  {
    "task": 1,
    "user": 2,
    "assigned_at": "2023-10-25T14:35:12.123456Z"
  }
]
```

### Get Tasks for a Specific User

**Request:**
```http
GET /api/users/1/tasks/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Implement login feature",
    "description": "Create login page with authentication",
    "created_at": "2023-10-25T14:30:45.123456Z",
    "task_type": "FEATURE",
    "completed_at": null,
    "status": "PENDING",
    "assigned_users": [
      {
        "id": 1,
        "username": "user1",
        "name": "John Doe",
        "email": "john@example.com",
        "mobile": "1234567890"
      },
      {
        "id": 2,
        "username": "user2",
        "name": "Jane Smith",
        "email": "jane@example.com",
        "mobile": "0987654321"
      }
    ]
  }
]
```

## Running Tests

```bash
python manage.py test
```

## Test Credentials

For testing the API, you can use the following test users (after creating them with the provided commands):

1. Admin User:
   - Username: admin
   - Password: admin123

2. Regular User:
   - Username: testuser
   - Password: password123

## Project Structure

The project follows a standard Django project structure with the following components:

- `task_management_project/` - Main project directory with settings
- `task_api/` - Application directory containing:
  - `models.py` - Data models for User, Task, and TaskAssignment
  - `serializers.py` - Serializers for API request/response handling
  - `views.py` - API views and viewsets
  - `urls.py` - URL routing configuration
  - `tests.py` - Test cases


