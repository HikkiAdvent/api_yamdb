## Проект YaMDb

## Описание проекта
Проект **YaMDb** собирает отзывы пользователей на различные произведения, такие как книги, фильмы или музыка. Пользователи могут оставлять отзывы, выставлять оценки и комментировать отзывы других пользователей. В зависимости от прав доступа, пользователи могут выполнять различные действия с контентом.


## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-логин/ваш-репозиторий.git
   ```
   
2. Перейдите в директорию проекта:
   ```bash
   cd ваш-репозиторий
   ```
3. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   python -m pip install --upgrade pip
   ```

4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Запуск проекта

1. Выполните миграции базы данных:
   ```bash
   python manage.py migrate
   ```

2. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

3. Перейдите в браузере по адресу: `http://127.0.0.1:8000/`

## Использование

В проекте реализованы следующие роли пользователей:

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — помимо просмотра, может публиковать отзывы, ставить оценки произведениям, комментировать отзывы, а также редактировать и удалять свои отзывы и комментарии.
- Модератор (moderator) — имеет те же права, что и пользователь, а также может удалять любые отзывы и комментарии.
- Администратор (admin) — имеет полные права на управление проектом, включая создание и удаление произведений, категорий и жанров, а также управление пользователями и их ролями.
- Суперюзер Django — имеет все права администратора.

## Основные эндпоинты API

### Пользователи и аунтификация:

* Регистрация нового пользователя: ```POST /api/v1/auth/signup/```
* Получение JWT-токена: ```POST /api/v1/auth/token/```
* Управление пользователями:
  * ```GET /api/v1/users/``` — список пользователей (для администратора).
  * ```POST /api/v1/users/``` — добавление пользователя (для администратора).
  * ```GET /api/v1/users/{username}/``` — получение данных пользователя по username.
  * ```PATCH /api/v1/users/{username}/``` — изменение данных пользователя.
  * ```DELETE /api/v1/users/{username}/``` — удаление пользователя (для администратора).
  * ```GET /api/v1/users/me/``` — данные своей учетной записи (для авторизованного пользователя).
  * ```PATCH /api/v1/users/me/``` — изменение данных своей учетной записи (для авторизованного пользователя).
### Контент: Категории, Жанры и Произведения

* Категории:
  * ```GET /api/v1/categories/``` — список всех категорий.
  * ```POST /api/v1/categories/``` — добавление категории (для администратора).
  * ```DELETE /api/v1/categories/{slug}/``` — удаление категории (для администратора).
* Жанры:
  * ```GET /api/v1/genres/``` — список всех жанров.
  * ```POST /api/v1/genres/``` — добавление жанра (для администратора).
  * ```DELETE /api/v1/genres/{slug}/``` — удаление жанра (для администратора).
* Произведения:
  * ```GET /api/v1/titles/``` — список всех произведений.
  * ```POST /api/v1/titles/``` — добавление произведения (для администратора).
  * ```PATCH /api/v1/titles/{title_id}/``` — частичное обновление (для администратора).
  * ```DELETE /api/v1/titles/{title_id}/``` — удаление произведения (для администратора).

### Отзывы и Комментарии

* Отзывы к произведениям:
  * ```GET /api/v1/titles/{title_id}/reviews/``` — список всех отзывов на произведение.
  * ```POST /api/v1/titles/{title_id}/reviews/``` — создание отзыва (для авторизованных пользователей).
  * ```GET /api/v1/titles/{title_id}/reviews/{review_id}/``` — получение отзыва по ID.
  * ```PATCH /api/v1/titles/{title_id}/reviews/{review_id}/``` — обновление (для автора, модератора или администратора).
  * ```DELETE /api/v1/titles/{title_id}/reviews/{review_id}/``` — удаление отзыва.

* Комментарии к отзывам:
  * ```GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/``` — все комментарии к отзыву.
  * ```POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/``` — создание комментария (для авторизованных пользователей).
  * ```GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/``` — получение комментария по ID.
  * ```PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/``` — обновление (для автора, модератора или администратора).
  * ```DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/``` — удаление.


## Примеры использования эндпоинтов API:

1. Регистрация пользователя
   
    ```https
    POST /api/v1/auth/signup/
    Content-Type: application/json
    {
        "username": "^w\\Z",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
    ```

2. Получение токена
   
    ```https
    POST /api/v1/auth/token/
    Content-Type: application/json
    {
        "username": "^w\\Z",
        "confirmation_code": "string"
    }
    ```

3. Частичное обновление информации о произведении
   
   ```https
    PATCH api/v1/titles/{titles_id}/
    Content-Type: application/json
    {
        "username": "^w\\Z",
        "confirmation_code": "string"
    }
    ```
4. Пример поиска и фильтрации:

   ```bash
   GET /api/v1/titles/?genre=drama&category=movie&year=2022
   ```

5. Пример поиска и фильтрации отзывов:

   ```bash
   GET /api/v1/titles/1/reviews/?search=great&ordering=-pub_date
   ```


## Тестирование

Опишите, как запустить тесты:
```bash
python manage.py test
```

## Кон Contributors

- Валерий Петренко - [Ваш GitHub](https://github.com/HikkiAdvent)
- Борисенко Виталий - [Ваш GitHub](https://github.com/bvv-praktikum)
- Чистяков Сергей - [Ваш GitHub](https://github.com/noxsir0)

## Лицензия
