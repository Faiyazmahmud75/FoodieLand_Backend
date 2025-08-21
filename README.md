# FoodieLand API (Django + DRF)

Community-driven recipes and blogs platform API.

## Quick start (local)
- Create virtualenv and install deps
```
python -m venv venv
./venv/Scripts/activate  # PowerShell
pip install -r requirements.txt
```
- Configure env
```
copy .env.example .env  # set SMTP later for real emails
```
- Run
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## OpenAPI docs
- `GET /api/docs/`

## Auth
- POST `/api/auth/register/`
- POST `/api/auth/token/` (JWT login)
- POST `/api/auth/token/refresh/`
- GET/PATCH `/api/auth/me/`
- POST `/api/auth/verify-email/`
- POST `/api/auth/request-password-reset/`
- POST `/api/auth/reset-password/`

## Recipes
- `/api/recipes/`
- `/api/recipes/categories/`
- `/api/recipes/my/ratings/`
- `/api/recipes/my/favorites/`

## Blogs
- `/api/blogs/`
- `/api/blogs/categories/`
- `/api/blogs/comments/?blog=<id>`
- POST `/api/blogs/{id}/increment_view/` 