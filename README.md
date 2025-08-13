# FoodieLand Backend

This is the **backend** for the FoodieLand platform — a community-driven site where users can share and explore recipes, write blogs, and connect with cooking enthusiasts.  
Built with **Django REST Framework** and **SQLite** for development.

---

## 🚀 Features
- **User Authentication** (JWT-based)
- **Recipes Management** (CRUD)
- **Blog Management** (CRUD)
- **Contact Form API**
- **User Profile Management**
- **Media & Static File Handling**
- **CORS Enabled** for React frontend
- **SQLite** for easy local development

---

## 🛠️ Technology Stack
- **Backend**: Django 4.x, Django REST Framework
- **Auth**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development) — can be switched to PostgreSQL for production
- **API Docs**: Swagger (drf-yasg)

---

## 📦 Installation & Setup

1. **Clone Repository**
```bash
git clone https://github.com/AKJilani/Foodieland_Backend.git
cd foodieland_backend

Create Virtual Environment
===========================
bash
Copy
Edit
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate


Install Dependencies
========================
pip install -r requirements.txt


Run Migrations
===========================
python manage.py migrate


Run Development Server
=====================
python manage.py runserver


foodieland_backend/
│── foodieland_backend/   # Project settings
│── users/                # User authentication & profile
│── recipes/              # Recipe API
│── blogs/                # Blog API
│── contact/              # Contact API
│── media/                # Uploaded files
│── db.sqlite3            # SQLite database
│── manage.py
│── requirements.txt
│── README.md


