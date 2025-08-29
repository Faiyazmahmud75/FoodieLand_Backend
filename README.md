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

🔐 Auth & User

POST /auth/register/ – Register

POST /auth/token/ – JWT login

POST /auth/token/refresh/ – Refresh token

GET /auth/me/ – Current user

PUT /auth/me/ – Update user

PATCH /auth/me/ – Partial update

POST /auth/firebase-verify-email/ – Verify email

POST /auth/request-password-reset/ – Request reset

POST /auth/reset-password/ – Reset password

🥘 Recipes

GET /recipes/ – List recipes

POST /recipes/ – Create recipe

GET/PUT/PATCH/DELETE /recipes/{id}/ – Recipe detail

GET/POST /recipes/categories/ – List/create category

GET/PUT/PATCH/DELETE /recipes/categories/{id}/ – Category detail

User-specific

GET /recipes/my/favorites/ – My favorites

POST /recipes/my/favorites/ – Add favorite

DELETE /recipes/my/favorites/{id}/ – Remove favorite

GET /recipes/my/ratings/ – My ratings

POST /recipes/my/ratings/ – Add rating

DELETE /recipes/my/ratings/{id}/ – Remove rating

📝 Blogs

GET/POST /blogs/blogs/ – List/create blogs

GET/PUT/PATCH/DELETE /blogs/blogs/{id}/ – Blog detail

POST /blogs/blogs/{id}/increment_view/ – Increment view

GET/POST /blogs/categories/ – List/create categories

GET/PUT/PATCH/DELETE /blogs/categories/{id}/ – Category detail

💬 Blog Comments

GET/POST /blogs/comments/ – List/add comment

GET/PUT/PATCH/DELETE /blogs/comments/{id}/ – Comment detail

🤝 Interactions

GET/POST /interactions/contact-messages/ – Personal messages

POST /interactions/contact-messages/{id}/reply/ – Reply to message

GET/POST /interactions/contact-us/ – Contact Us messages

GET/POST /interactions/follows/ – Follow users

POST /interactions/follows/unfollow/ – Unfollow

GET/POST /interactions/newsletter/ – Subscribe newsletter

GET /interactions/users/ – List all users

✅ Users (Read-only)

GET /users/ – List users

GET /users/{id}/ – User detail
