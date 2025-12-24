# Backend API Guide (Logbook Project)

This document provides documentation for frontend developers to integrate with the backend API.

## Authentication

The application uses Django session-based authentication.

### Login
- **URL**: `/` (Base path)
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password",
    "remember": "true/false" (optional)
  }
  ```
- **Note**: Successful login redirects to `/dashboard/`.

### Signup
- **URL**: `/signup/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "unique_username",
    "email": "user@example.com",
    "confirm_password": "secure_password",
    "currency": "USD" (ISO code)
  }
  ```

### Logout
- **URL**: `/logout/`
- **Method**: `POST`

---

## API Endpoints

All API endpoints are prefixed with `/api/`. They require an authenticated session.

### 1. Get User Info
- **URL**: `/api/main/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "message": "Hello, username!"
  }
  ```

### 2. Get Tasks
- **URL**: `/api/get-task/`
- **Method**: `GET`
- **Query Params**: `date` (format: `YYYY-MM-DD`, optional)
- **Response**: Array of Task objects.

### 3. Create Task
- **URL**: `/api/set-task/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "date": "2025-12-24T12:00:00Z",
    "start": "09:00:00",
    "end": "17:00:00",
    "job_name": "Developer",
    "hourly_rate": "50.00",
    "break_duration": 30,
    "payment_status": false
  }
  ```

### 4. Edit Task
- **URL**: `/api/edit-task/`
- **Method**: `POST`
- **Body**: Include `id` and any fields to update.
  ```json
  {
    "id": 1,
    "job_name": "Senior Developer"
  }
  ```

### 5. Delete Task
- **URL**: `/api/delete-task/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "id": 1
  }
  ```

### 6. Summary Statistics
- **URL**: `/api/summary/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "total_entries": 10,
    "total_hours": 80.5,
    "total_earnings": 4025.0,
    "total_paid": 5,
    "total_unpaid": 5
  }
  ```

---

## Data Models

### Task Object
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Unique identifier (read-only) |
| `date` | DateTime | Task date |
| `start` | Time | Start time (HH:MM:SS) |
| `end` | Time | End time (HH:MM:SS) |
| `job_name` | String | Name of the job |
| `hourly_rate` | Decimal | Rate per hour |
| `break_duration` | Integer | Break in minutes |
| `payment_status` | Boolean | Whether paid or due |

---

## Global Currencies
Available at `/signup/` via `GET` context or hardcoded in `book/views.py`. Uses ISO 4217 codes (e.g., `USD`, `EUR`, `GBP`).
