# LogBook - Professional Shift Tracker

LogBook is a modern, high-fidelity web application designed for workers and freelancers to track their shifts, hours, and earnings with precision. It features a premium dark-themed dashboard, responsive design, and robust data management.

## 👥 Credits

- **Frontend Development**: Gemini 3 Flash
- **Backend Infrastructure**: [GitHub User]

## ✨ Key Features

- **Dynamic Dashboard**: A premium user experience with:
  - **Desktop View**: Comprehensive tabular data display.
  - **Mobile View**: Creative, touch-friendly card-based layout.
- **Smart Shift Logging**:
  - Track `Job Description`, `Start Time`, `End Time`, and `Hourly Rate`.
  - **Auto-Calculations**: Dynamic earnings calculation based on net hours worked.
  - **Break Management**: Automatically deducts break duration from total payable hours.
  - **Validation**: Built-in checks to ensure end times are after start times and breaks don't exceed shift duration.
- **Statistical Summary**: Centered modal providing:
  - Total hours worked (with overnight shift support).
  - Total earnings across all tasks.
  - Paid vs. Unpaid entry tracking.
- **Secure Authentication**:
  - Session-based login with "Remember Me" support.
  - Comprehensive signup with a **Global Currency Selector** (100+ currencies).
  - Frontend password confirmation validation.

## 🛠 Tech Stack

- **Backend**: Django & Django REST Framework (DRF)
- **Database**: PostgreSQL (Cloud-hosted with SSL support)
- **Frontend**: Vanilla HTML5, CSS3 (Custom Design System), and Moduler JavaScript.
- **Security**: HTTPS/SSL Integration, CSRF Protection, and IsAuthenticated Permissions.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- PostgreSQL Database

### 2. Installation
Clone the repository and install the required dependencies:
```bash
pip install django djangorestframework django-sslserver python-dotenv psycopg2-binary
```

### 3. Environment Setup
Create a `.env` file in the root directory and add your database credentials:
```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```

### 4. Database Setup
Register the models and migrate the schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Running the Application
To run the server with SSL (recommended for session security):
```bash
python manage.py runsslserver
```
Visit `https://127.0.0.1:8000/` in your browser.

## 🌐 Hosting on Render

LogBook is pre-configured for easy deployment to **Render**.

### 1. Preparation
Ensure you have a `requirements.txt` file (already included) and your changes are pushed to a Git repository.

### 2. Create a Web Service
- Connect your GitHub/GitLab account to Render.
- Select your repository.
- **Environment**: `Python`
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command**: `gunicorn logbook.wsgi`

### 3. Environment Variables
Add the following variables in the **Environment** tab of your Render service:
- `DEBUG`: `False` (for production)
- `SECRET_KEY`: Your secret key
- `DATABASE_URL`: Your PostgreSQL connection string (Render provides this if using their Database service)
- `ALLOWED_HOSTS`: `your-app-name.onrender.com`
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`: (If not using `DATABASE_URL`)

## 🎨 Design Principles
LogBook uses a deep grey/black palette with a soft cyan accent (`#9ed0f8`). The UI utilizes glassmorphism, subtle micro-animations, and a mobile-first philosophy to ensure a premium feel across all devices.

---
*Version 1.2.2.0*
