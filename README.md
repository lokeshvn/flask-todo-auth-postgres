# ✅ Flask Todo App with Auth & PostgreSQL

Simple **per‑user Todo List** web app built with **Flask**, **PostgreSQL**, **Flask‑Login**, **SQLAlchemy**, and **Bootstrap 5**.

## Live Demo

https://flask-todo-app-fk2x.onrender.com/
---

## 🚀 Features

- 🔐 User registration & login with secure password hashing (Werkzeug + Flask‑Login).
- 👤 Each user has their **own** todo list (User → Todo one‑to‑many).
- 📝 Todo CRUD:
  - ➕ Add new todo
  - 🔁 Toggle completed / pending
  - 🗑️ Delete todo
- 🗄️ Persistent storage in PostgreSQL via Flask‑SQLAlchemy.
- 🎨 Clean, responsive UI using Bootstrap 5 (CDN).

---

## 🧰 Tech Stack

- 🐍 Backend: **Flask** (Python)
- 🗃️ Database: **PostgreSQL**
- 🧬 ORM: **Flask‑SQLAlchemy**
- 🔑 Auth: **Flask‑Login** + **Werkzeug security**
- 🧩 Templating: **Jinja2**
- 🎀 Styling: **Bootstrap 5** via CDN

---

## ⚙️ Setup & Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/lokeshvn/flask-todo-auth-postgres.git
   cd flask-todo-auth-postgres
2. Create and activate virtual environment

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
# source venv/bin/activate

3. Install dependencies

   pip install -r requirements.txt
   
4. Create PostgreSQL database

  Database name: tododb

  User: postgres

  Password: your password

5. Configure database URI

In app.py:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:YOUR_PASSWORD@localhost:5432/tododb'

6. Run the app

   flask --app app run
   
8. Open in browser

   http://127.0.0.1:5000


📌 Usage
📝 Register a new user account.

🔑 Login with your credentials.

✅ Add / toggle / delete todos in your personal list.

🚪 Logout when you’re done.

📚 Learning Goals
This project was built to practice:

  >Structuring a small Flask app with authentication.
  
  >Using PostgreSQL with SQLAlchemy models & relationships.
  
  >Protecting routes with @login_required and current_user.
  
  >Styling server‑rendered pages using Bootstrap quickly.

👨‍💻 Author: Lokesh V N
💼 Stack: Python · Flask · PostgreSQL · Bootstrap
