# Tasks API with FastAPI and PostgreSQL

A tasks API where you can manage complex projects by assigning different tasks to members. Whenever a new task is created or a task is reassigned, the person getting the task gets an email with Celery background tasks with RabbitMQ message broker.

## Technologies-
- Python 3.13.5
- FastAPI 0.116.1
- PostgreSQL
- Celery
- RabbitMQ

---

## Project Setup-

### 1. Clone the repo
```bash
git clone https://github.com/singhakshitraj/tasks-api.git
```

### 2. Install dependencies for project
```bash
pip install -r requirements.txt
```

### 3. Configure Project

#### 1. For Setting Up PostgreSQL Database
```sql
CREATE DATABASE TASKS
```

#### 2. For migrating db-tables  
From the project root directory, run command:
```sql
\i 'db/schemas/user.sql';
\i 'db/schemas/project.sql';
\i 'db/schemas/tasks.sql';
```

#### 3. Setup Environment Variables
```env
# RABBITMQ URL
CLOUDAMQP_URL=__YOUR_RABBITMQ_URL__

# DB Variables
HOST=__YOUR_DB_HOST__
PORT=__YOUR_DB_PORT__
USER=__YOUR_DB_USER__
PASSWORD=__YOUR_DB_PASSWORD__
DB_NAME=__YOUR_DB_NAME__

# For JWT-AUTH
SECRET_KEY=__YOUR_SECRET_KEY__ // Unique SECRET-KEY to encrypt and decrypt token
ALGORITHM=__YOUR_JWT_ALGORITHM__

# For Using Mail Services
MAIL_USERNAME=__YOUR_EMAIL_ADDRESS__
MAIL_PASSWORD=__YOUR_APP_PASSWORD__
MAIL_FROM=__YOUR_EMAIL_ADDRESS__
MAIL_PORT=__YOUR_EMAIL_PORT__
MAIL_SERVER=__YOUR_SMTP_SERVER__
MAIL_STARTTLS=__TRUE_OR_FALSE__
MAIL_SSL_TLS=__TRUE_OR_FALSE__
USE_CREDENTIALS=__TRUE_OR_FALSE__
VALIDATE_CERTS=__TRUE_OR_FALSE__
```

---

### 4. Run Application-
#### 1. DEV MODE
```bash
uvicorn main:app --reload
celery -A celery_worker.celery_ap worker -Q emails
```

- `-Q emails`  
  Celery listens to messages in the emails queue.  
- `--pool=solo`  
  For running celery on windows, add `--pool=solo` because celery uses some package that requires multiprocessing requiring somethign which windows does provide access to, so we need to mention to use without caring about multiprocessing.  
- `--loglevel=info`  
  For getting information about the celery during devmode.

---
## Database Design
<img width="1303" height="807" alt="Screenshot 2025-08-07 201936" src="https://github.com/user-attachments/assets/58e4e6d8-da02-40e9-a8de-64130bd8943a" />

## Code Structure

This project is modularized into several folders, each responsible for a specific functionality. The main components are:

- **db**: Handles database schemas and connection setup.
- **routers**: Contains API route definitions for various resources.
- **utils**: Holds helper utilities for authentication, email sending, and access checks.
- **validation_models**: Defines request/response models for validation using Pydantic.
- **celery_worker.py**: Configures and runs Celery for background task processing.
- **main.py**: The FastAPI application entry point.

```
/db
│
├── connection.py      # Database connection setup.
└── schemas/           # SQL schema files for creating tables and indexes.
    ├── project.sql    |
    ├── tasks.sql      |-- Schema for PostgreSQL
    └── user.sql       |

/routers
├── auth.py            |
├── project.py         |-- API Endpoints for management
└── task.py            |

/utils
├── check_access.py    
├── current_user.py    # Retrieves the current authenticated user.
├── password.py
└── send_email.py      # Email sending functionality.

/validation_models	
├── project.py         |-- Validation Models for requests/responses 
└── task.py            |

.env                   # Environment variables configuration.
.gitignore          
celery_worker.py       # Celery worker setup for background tasks.
main.py                
readme.md              
```

---

## Usage

The API can be accessed at localhost/docs or localhost/redoc
