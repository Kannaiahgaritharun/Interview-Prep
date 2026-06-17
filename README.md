# Interview Preparation Portal

A complete full-stack web application for tracking coding interview preparation. Built with FastAPI, PostgreSQL, SQLAlchemy, and a Bootstrap-based frontend.

## Features
- **User Authentication**: Secure registration and login using JWT and password hashing.
- **Dashboard Analytics**: View total solved questions, topic breakdown, and upcoming revisions.
- **Question Management**: Add, view, filter (by topic/difficulty), and search interview questions.
- **Progress Tracking**: Track solved/unsolved status, save notes, and schedule revision dates.

## Technology Stack
- **Backend**: Python 3.12+, FastAPI, Uvicorn
- **Database**: PostgreSQL, SQLAlchemy ORM, Alembic
- **Security**: JWT (HttpOnly Cookies), Passlib (Bcrypt)
- **Frontend**: HTML, CSS, JavaScript (Fetch API), Bootstrap 5, Jinja2 Templates

## Setup Instructions

### 1. Prerequisites
- Python 3.12+
- PostgreSQL
- Docker (optional, for easy database setup)

### 2. Database Configuration
You can use the provided `docker-compose.yml` to spin up a PostgreSQL instance:
```bash
docker-compose up -d
```
Alternatively, create a database named `interview_db` in your local PostgreSQL server and update the `.env` file with your credentials.

### 3. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run Migrations (Optional)
The application is configured to automatically create tables on startup. However, you can use Alembic for future migrations:
```bash
alembic upgrade head
```

### 5. Start the Application
```bash
uvicorn app.main:app --reload
```
The portal will be available at `http://127.0.0.1:8000`.

## API Endpoints
- **Auth**: `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`
- **Questions**: `/api/questions/` (GET, POST), `/api/questions/{id}` (GET, PUT, DELETE)
- **Progress**: `/api/progress/` (GET, POST), `/api/progress/{id}` (GET)
- **Dashboard**: `/api/dashboard/` (GET)

## Future Improvements
- Pagination for questions.
- Email verification.
- Dark mode support.
- User profile settings.
