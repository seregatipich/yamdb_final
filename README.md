![finaltask](https://github.com/seregatipich/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# yamdb_final
yamdb_final

проект здесь - http://158.160.44.238/redoc/ и http://158.160.44.238/api/v1/
# API_YamDB

REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке.

Проект YaMDb собирает отзывы пользователей на произведения. 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр. Новые жанры и категории может создавать только администратор.
Читатели оставляют к произведениям текстовые отзывы и выставляют произведению рейтинг (оценку в диапазоне от 1 до 10).
Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.
На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

Аутентификация по JWT-токену

Поддерживает методы GET, POST, PUT, PATCH, DELETE

Предоставляет данные в формате JSON

Cоздан в команде из трёх человек с использованим Git в рамках учебного курса Яндекс.Практикум.

Команда: Артем, Георгий, Сергей.

## Технологии
- проект написан на Python с использованием Django REST Framework
- библиотека Simple JWT - работа с JWT-токеном
- библиотека django-filter - фильтрация запросов
- база данны - SQLite3
- система управления версиями - git

## Как запустить проект?

1) Клонируйте репозитроий с проектом:
```
git clone https://github.com/Darkteman/api_yamdb.git
```
2) В созданной директории установите виртуальное окружение, активируйте его и установите необходимые зависимости:
```
python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt
```
3) Выполните миграции:
```
python manage.py migrate
```
4) Cоздайте суперпользователя:
```
python manage.py createsuperuser
```
5) Загрузите тестовые данные:
```
python manage.py closepoll
```
6) Запустите сервер:
```
python manage.py runserver
```
__________________________________

Ваш проект запустился на http://127.0.0.1:8000/

Полная документация [redoc.yaml] доступна по адресу http://127.0.0.1:8000/redoc/

С помощью команды *pytest* вы можете запустить тесты и проверить работу модулей

## Алгоритм регистрации пользователей
- Пользователь отправляет запрос с параметрами *email* и *username* на */api/v1/auth/signup/*.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес *email* .
- Пользователь отправляет запрос с параметрами *email* и *confirmation_code* на */api/v1/auth/token/*, в ответе на запрос ему приходит token (JWT-токен).

## Ресурсы API YaMDb

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). 
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
______________________________________________________________________
### Пример http-запроса (POST) для создания нового комментария к отзыву:
```
url = 'http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/'
data = {'text': 'Your comment'}
headers = {'Authorization': 'Bearer your_token'}
```
### Ответ API_YamDB:
```
Статус- код 200

{
 "id": 0,
 "text": "string",
 "author": "string",
 "pub_date": "2022-11-20T14:15:22Z"
}
```
пример