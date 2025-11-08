# ToDoList API

FastAPI-based backend for a to-do list application that supports user registration, authentication, and task management. The service uses SQLAlchemy for persistence, Alembic for migrations, and issues JWT access tokens that are echoed in both the JSON response and an HTTP-only cookie.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Layout](#project-layout)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Setup](#setup)
- [Database & Migrations](#database--migrations)
- [Running the Server](#running-the-server)
- [API Reference](#api-reference)
  - [Auth & User](#auth--user)
  - [Task Management (Protected)](#task-management-protected)
- [Contributing](#contributing)

## Features
- User registration with unique username & email validation.
- Passwords hashed with bcrypt before persistence.
- JWT access tokens returned in the login response and persisted in an HTTP-only cookie.
- OAuth2-style authentication using `OAuth2PasswordBearer` for protected routes.
- Task CRUD endpoints tied to the authenticated user with validation for titles and ownership rules.
- Alembic-powered migrations aligned with SQLAlchemy models.

## Tech Stack
- **Language:** Python 3.13+
- **Framework:** FastAPI
- **Database:** Configurable through `DATABASE_URL` (e.g., PostgreSQL, SQLite)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Auth:** JWT (PyJWT + python-jose) & OAuth2PasswordBearer
- **Other libraries:** bcrypt, python-dotenv

## Project Layout
```
app/
├── api/
│   └── v1/
│       ├── routes_user.py          # Registration & login
│       └── routes_protected.py     # Authenticated user & task endpoints
├── auth.py                         # Token decoding helpers
├── core/
│   └── config.py                   # Environment-driven settings
├── db/
│   ├── base.py                     # SQLAlchemy Base
│   ├── session.py                  # SessionLocal & engine
│   └── init_db.py                  # (placeholder)
├── main.py                         # FastAPI app entry point
├── models/                         # SQLAlchemy models (User, Tasks)
├── repositories/                   # DB interaction logic
├── schemas/                        # Pydantic request / response models
└── services/                       # Service layer orchestrating repositories

alembic/
├── env.py                          # Alembic configuration bootstrap
└── versions/                       # Auto-generated migration scripts
```

## Prerequisites
- Python 3.13 or newer (matching the project venv)
- PostgreSQL / SQLite / compatible database (driven by `DATABASE_URL`)
- Pip / virtualenv tools

## Environment Variables
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/todolist
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
> Adjust `DATABASE_URL` for your driver (e.g., `sqlite:///./app.db`).

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows PowerShell
pip install -r requirements.txt   # Ensure this file lists FastAPI, SQLAlchemy, Alembic, bcrypt, python-dotenv, python-jose, PyJWT, etc.
```
> If `requirements.txt` is missing, install manually:
> ```bash
> pip install fastapi uvicorn[standard] SQLAlchemy alembic python-dotenv bcrypt python-jose pyjwt passlib
> ```

## Quickstart
1. Clone the repo and `cd` into it.
2. Create & activate the virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your `.env` file (see [Environment Variables](#environment-variables)).
5. Run migrations to create/update the schema:
   ```bash
   alembic upgrade head
   ```
6. Start the API server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Database & Migrations
Ensure models are imported in `