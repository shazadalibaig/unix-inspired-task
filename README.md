# 🧪 Unix-Inspired Task Manager API

A lightweight task management backend inspired by Unix process operations. This Django-based REST API allows users to list tasks (`GET /tasks/`) like `ls` and spawn new tasks (`POST /tasks/`) like `fork`.

---

## 🚀 Features

- ✅ Create new tasks (simulating a "fork" operation)
- 📄 List all tasks (like `ls`)
- ✏️ Update tasks
- ❌ Delete tasks
- ⚠️ Validations & error handling
- 🧪 Unit & integration tests included

---

## 🛠 Tech Stack

- Python 3.13
- Django 5.2
- Django REST Framework (DRF)
- SQLite (default, easy switch to PostgreSQL)

---

## 📦 Setup Instructions

### 1️⃣ Clone the repo

```bash
git clone https://github.com/shazadalibaig/unix-inspired-task.git
cd taskmanager
```

### 2️⃣ Create virtual environment

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

### 3️⃣ Install dependencies

pip install -r requirements.txt

### 4️⃣ Apply migrations

python manage.py migrate

### 5️⃣ Run server

python manage.py runserver

🔗 API Endpoints

📋 List Tasks

api/v1/tasks/

### Response:

[
{
"id": 1,
"name": "Sample Task",
"status": "running",
"created_at": "2025-04-21T14:32:05Z",
}
]

➕ Create Task

api/v1/tasks/

### Request Body:

{
"name": "New Task",
"status": "running"
}

### Response:

{
"id": 2,
"name": "New Task",
"status": "running",
"created_at": "...",
}
🔁 If a task with the same name exists and is still running, a new task won't be created.

🛠 Update Task

api/v1/tasks/<int:pk>/

❌ Delete Task

api/v1/tasks/<int:pk>/

✅ Validations:

Task name is required and must be non-empty.

Only one running task with the same name is allowed at a time.

Status must be either: running, completed.

🧪 Running Tests

python manage.py test tasks

### Includes:

✅ CRUD tests

⚠️ Edge case validations

🚫 Error handling for invalid requests

🧑‍💻 Author

Mohammad Shazadali Baig
Python Developer | API Enthusiast | Clean Coder
