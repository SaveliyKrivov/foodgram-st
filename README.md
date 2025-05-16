# Foodgram

Проект Foodgram — «Продуктовый помощник»: приложение для публикации рецептов, добавления их в избранное и список покупок, а также подписки на авторов.

## 🚀 Быстрый старт

Клонируйте репозиторий:

```bash
git clone https://github.com/SaveliyKrivov/foodgram-st.git
cd foodgram-st
```
В корне проекта разместите .env файл. Структура:
```
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
SECRET_KEY = 'django-insecure-example-key'
DEBUG = False
ALLOWED_HOSTS=127.0.0.1,localhost
```
### Соберите и запустите проект:
В папке backend/infra/
```bash
docker-compose up -d --build
```
Примените миграции, соберите статику и создайте суперпользователя:

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
docker-compose exec backend python manage.py createsuperuser
```
### 📦 Загрузка данных
Загрузите ингредиенты, пользователей и рецепты:

```bash
docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py load_users
docker-compose exec backend python manage.py load_recipes
```
