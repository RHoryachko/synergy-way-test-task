# Synergy Way Test Task

A FastAPI application that periodically fetches user data, posts, and comments from external APIs and stores them in a PostgreSQL database. The application uses Celery for background task processing and provides a REST API to view the collected data.

## Features

- Periodic data fetching from external APIs using Celery Beat
- User, post, and comment data management
- REST API for viewing stored data
- Docker-based setup for easy deployment
- Automated testing with pytest

## Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **Celery** - Distributed task queue for background jobs
- **PostgreSQL** - Relational database
- **Redis** - Message broker for Celery
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **pytest** - Testing framework
- **Docker & Docker Compose** - Containerization

## Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd synergy-way-test-task
```

2. Create a `.env` file in the root directory (optional, defaults are provided):
```env
POSTGRES_USER=synergy
POSTGRES_PASSWORD=synergy123
POSTGRES_DB=synergy_db
DATABASE_URL=postgresql://synergy:synergy123@db:5432/synergy_db
REDIS_URL=redis://redis:6379/0
ENV=development
```

3. Build and start the services:
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Redis server (port 6379)
- FastAPI web server (port 8000)
- Celery worker
- Celery beat scheduler

## API Endpoints

Once the application is running, you can access the API at `http://localhost:8000`

### Health Check
- `GET /health` - Check application status

### Users
- `GET /users` - Get list of users (with pagination: `?skip=0&limit=10`)
- `GET /users/{user_id}` - Get user by ID
- `GET /users/{user_id}/posts` - Get all posts for a user

### Posts
- `GET /posts` - Get list of posts (with pagination: `?skip=0&limit=10`)
- `GET /posts/{post_id}` - Get post by ID
- `GET /posts/{post_id}/comments` - Get all comments for a post

### Comments
- `GET /comments` - Get list of comments (with pagination: `?skip=0&limit=10`)

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Scheduled Tasks

The application automatically fetches data from external APIs:

- **Users**: Fetched from `jsonplaceholder.typicode.com` every 5 minutes
- **Posts**: Fetched from `dummyjson.com` every 10 minutes
- **Comments**: Fetched from `dummyjson.com` every 10 minutes

Data is fetched gradually (incrementally) to avoid loading everything at once.

## Running Tests

To run the test suite:

```bash
docker-compose exec web pytest -v
```

Or with coverage:

```bash
docker-compose exec web pytest --cov=app tests/
```

## Project Structure

```
app/
├── routers/          # API endpoint definitions
├── services/         # Business logic layer
├── models.py         # Database models
├── schemas.py        # Pydantic schemas
├── tasks.py          # Celery tasks
├── celery_app.py     # Celery configuration
├── config.py         # Application settings
├── database.py       # Database connection setup
└── main.py           # FastAPI application entry point

tests/                # Test files
```

## Development

The application uses hot-reload for development. Changes to Python files will automatically restart the FastAPI server.

To view logs:
```bash
docker-compose logs -f web
docker-compose logs -f worker
docker-compose logs -f beat
```

## Stopping the Application

To stop all services:
```bash
docker-compose down
```

To stop and remove volumes (clean database):
```bash
docker-compose down -v
```
