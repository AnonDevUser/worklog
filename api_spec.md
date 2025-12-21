# Logbook API Specification

This document defines the contract between the frontend (JavaScript) and the backend (Django REST Framework). 

## Base URL
All endpoints are relative to `/api/`.

## Authentication
Authentication is expected to be handled via Django session or Token authentication.
CSRF tokens must be included in the `X-CSRFToken` header for all `POST`, `PUT`, `PATCH`, and `DELETE` requests.

## Frontend UI (Loaders)
The frontend JavaScript client (`api.js`) automatically manages a global loader overlay (`#global-loader`). 
- **Start:** The loader is displayed immediately before the fetch request starts.
- **End:** The loader is hidden in a `finally` block, ensuring it disappears even if the request fails.
- **Backend Impact:** None. This is a purely visual enhancement for smoother flow.

---

## Endpoints

### 1. Main Info
Returns a simple welcome message or initial state.
- **URL:** `/api/main/`
- **Method:** `GET`
- **Response:**
  - `200 OK`: `{"message": "string"}`

### 2. Get Tasks
Retrieves a list of tasks for the authenticated user.
- **URL:** `/api/get-task/`
- **Method:** `GET`
- **Query Parameters:**
  - `date` (optional): Filter by ISO date string (YYYY-MM-DD).
- **Response:**
  - `200 OK`: 
    ```json
    [
      {
        "id": 1,
        "date": "2023-10-27T10:00:00Z",
        "start": "09:00:00",
        "end": "17:00:00",
        "job_name": "Web Design",
        "payment_status": false,
        "user": 1
      }
    ]
    ```

### 3. Create Task
Creates a new log entry.
- **URL:** `/api/set-task/`
- **Method:** `POST`
- **Payload:**
  ```json
  {
    "date": "2023-10-27T10:00:00Z",
    "start": "09:00:00",
    "end": "17:00:00",
    "job_name": "Debugging",
    "payment_status": false
  }
  ```
- **Response:**
  - `201 Created`: The created task object.
  - `400 Bad Request`: Validation errors.

### 4. Edit Task
Updates an existing task.
- **URL:** `/api/edit-task/`
- **Method:** `POST` (or `PUT/PATCH` depending on implementation preference, placeholders currently use POST)
- **Payload:**
  ```json
  {
    "id": 1,
    "job_name": "Updated Job Name",
    "payment_status": true
  }
  ```
- **Response:**
  - `200 OK`: The updated task object.
  - `404 Not Found`: Task does not exist.

### 5. Summary
Returns a calculated summary of work (e.g., total hours, total earnings).
- **URL:** `/api/summary/`
- **Method:** `GET`
- **Response:**
  - `200 OK`:
    ```json
    {
      "total_entries": 10,
      "total_hours": 45.5,
      "total_paid": 5,
      "total_unpaid": 5
    }
    ```

---

## Error Handling
The API should return standard HTTP status codes:
- `400`: Bad Request (Invalid data)
- `401`: Unauthorized (Not logged in)
- `403`: Forbidden (CSRF failure or Permission denied)
- `500`: Internal Server Error
