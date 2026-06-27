# TaskPro Backend — Django REST Framework

AI-powered Task Manager REST API built with Django, PostgreSQL, and Google Gemini / Groq AI.

---

## How to Run Locally

### Prerequisites
- Python 3.11+
- PostgreSQL running locally
- pip

### Steps

**1. Clone the repo**
```bash
git clone https://github.com/MrGroot01/Taskpro-backend.git
cd Taskpro-backend
```

**2. Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create PostgreSQL database**
```sql
CREATE DATABASE taskpro_db;
```

**5. Create `.env` file**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=taskpro_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432

GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**6. Run migrations**
```bash
python manage.py migrate
```

**7. Start server**
```bash
python manage.py runserver
```

API runs at: `http://localhost:8000`

---

## Tech Stack & Why I Chose It

| Technology | Why |
|------------|-----|
| **Django 4.2** | Mature, batteries-included framework with excellent ORM and admin panel |
| **Django REST Framework** | Industry-standard for building REST APIs in Python |
| **PostgreSQL** | Reliable relational database, perfect for structured task data |
| **JWT (SimpleJWT)** | Stateless authentication, scales well, no session storage needed |
| **Groq + Gemini AI** | Groq is fast and free with generous limits; Gemini as fallback |
| **Gunicorn** | Production-grade WSGI server for deployment |
| **Whitenoise** | Serves static files efficiently without a separate CDN |
| **Render** | Free cloud hosting with built-in PostgreSQL support |

---

## API Endpoints

### Auth
```
POST   /api/accounts/register/        Register new user
POST   /api/accounts/login/           Login (returns JWT tokens)
POST   /api/accounts/token/refresh/   Refresh access token
POST   /api/accounts/logout/          Blacklist refresh token
GET    /api/accounts/profile/         Get user profile
PUT    /api/accounts/profile/         Update profile
```

### Tasks
```
GET    /api/tasks/           List tasks (filter: ?status=todo&priority=high&search=bug)
POST   /api/tasks/           Create task
GET    /api/tasks/:id/       Get task detail
PUT    /api/tasks/:id/       Update task
PATCH  /api/tasks/:id/       Partial update
DELETE /api/tasks/:id/       Delete task
GET    /api/tasks/stats/     Dashboard stats
POST   /api/tasks/reorder/   Drag and drop reorder
```

### AI
```
POST   /api/ai/suggest/      Generate title, description, priority from rough task title
                             Body: { "title": "fix login bug" }
```

---

## AI Tools, Libraries & Resources Used

- **Google Gemini 1.5 Flash** — Primary AI model for task suggestions
- **Groq llama-3.3-70b-versatile** — Fallback AI, faster and no daily limits
- **djangorestframework-simplejwt** — JWT authentication with token blacklisting
- **django-filter** — Query filtering for tasks by status and priority
- **django-cors-headers** — Cross-origin request handling for frontend
- **Django REST Framework Docs** — API design and serializer reference

---

## One Thing I Would Improve With More Time

**Smarter AI with caching and streaming** — Currently the AI generates a response and returns it all at once. With more time I would add response streaming so the suggestion appears word by word like ChatGPT, implement Redis caching so repeated similar titles return instantly without burning API quota, and add Claude as a third AI fallback. I would also add Celery + Redis for background tasks like sending email reminders for overdue tasks, and implement team workspaces so multiple users can collaborate on shared task boards.

---

## Live Demo

- **Frontend:** https://task-frontend-ndgz-a9w18ei6k-mrgroot01s-projects.vercel.app/
- **Backend:** https://taskpro-backend-96wu.onrender.com

## Repositories

- **Frontend:** https://github.com/MrGroot01/Task-frontend
- **Backend:** https://github.com/MrGroot01/Taskpro-backend
