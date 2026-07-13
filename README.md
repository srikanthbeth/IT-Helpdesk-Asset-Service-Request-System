# IT Helpdesk Asset Service Request System

## Project Overview

The IT Helpdesk Asset Service Request System is a FastAPI-based backend application that helps organizations manage IT assets and employee service requests. The system provides secure authentication using JWT, role-based authorization, asset management, service request tracking, request assignment, reporting, and pagination.

---

## Features

### Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing using Passlib

### Roles

- Admin
- IT Support
- Employee

### Asset Management

- Add Asset
- View All Assets
- View Asset by ID
- Update Asset
- Delete Asset
- Unique Asset Tag Validation

### Service Request Management

- Create Service Request
- View Service Requests
- Update Service Request
- Track Request Status

### Request Assignment

- Assign Service Request to IT Support
- View Assigned Requests

### Reports

- View Requests by Employee
- View Requests by Asset
- Filter by Priority
- Filter by Status
- Pagination Support

---

## Business Rules

- One asset can have multiple service requests.
- Asset tag must be unique.
- Closed requests cannot be edited.
- Only assigned IT Support can update request status.
- Resolution date is automatically recorded when the request status becomes Resolved.
- Employees can create and view only their own requests.
- IT Support can manage only assigned requests.
- Admin has access to all modules.

---

## Technology Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Passlib (bcrypt)
- Uvicorn
- Pytest

---

## Project Structure

```
it_helpdesk_asset_service_request_system/
│
├── routers/
│   ├── auth.py
│   ├── assets.py
│   ├── requests.py
│   ├── assignment.py
│   ├── reports.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_assets.py
│   ├── test_requests.py
│   ├── test_assignment.py
│   └── test_reports.py
│
├── auth.py
├── crud.py
├── database.py
├── dependencies.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository_url>
```

### Navigate to Project

```bash
cd it_helpdesk_asset_service_request_system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
uvicorn main:app --reload
```

Application URL

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|----------|----------------|------------------------|
| POST | /auth/register | Register User |
| POST | /auth/login | User Login |

### Asset Management

| Method | Endpoint | Description |
|----------|----------------|------------------------|
| POST | /assets | Create Asset |
| GET | /assets | View All Assets |
| GET | /assets/{id} | View Asset |
| PUT | /assets/{id} | Update Asset |
| DELETE | /assets/{id} | Delete Asset |

### Service Requests

| Method | Endpoint | Description |
|----------|----------------|------------------------|
| POST | /requests | Create Request |
| GET | /requests | View All Requests |
| GET | /requests/{id} | View Request |
| PUT | /requests/{id} | Update Request |

### Assignment

| Method | Endpoint | Description |
|----------|----------------|------------------------|
| POST | /requests/{request_id}/assign/{support_id} | Assign Request |
| GET | /support/{support_id}/requests | Assigned Requests |

### Reports

| Method | Endpoint | Description |
|----------|----------------|------------------------|
| GET | /reports/employee/{employee_id} | Employee Requests |
| GET | /reports/asset/{asset_id} | Asset Requests |
| GET | /reports | Filter by Priority |
| GET | /reports | Filter by Status |
| GET | /reports?page=1&limit=10 | Pagination |

---

## Authentication

The application uses JWT Authentication.

Login using:

```
POST /auth/login
```

Use the generated access token to authorize protected endpoints through Swagger UI.

---

## Testing

Run all test cases using:

```bash
pytest
```

or

```bash
python -m pytest
```

---

## Validation

- Asset Tag must be unique.
- Email must be unique.
- JWT Token validation.
- Role-Based Authorization.
- Closed requests cannot be modified.
- Assigned IT Support only can update request status.

---

## Database

SQLite Database

```
helpdesk.db
```

---

## Future Enhancements

- Email Notifications
- Dashboard Analytics
- File Upload for Assets
- Asset Maintenance History
- Password Reset
- Audit Logs

---

## Author

**Name:** Srikanth Bethamcharla

Backend Project developed using FastAPI, SQLAlchemy, SQLite, JWT Authentication, and REST APIs.
