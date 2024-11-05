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

3. Установите зависимости:
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

* Регистрация нового пользователя: ```http
   POST /api/v1/auth/signup/```
* Получение JWT-токена: ```POST /api/v1/auth/token/```
* Категории:
  * Получение всех категорий: ```GET /api/v1/categories/```
  * Создание категории: ```POST /api/v1/categories/``` (только для администратора)
  * Удаление категории: ```DELETE /api/v1/categories/{slug}/``` (только для администратора)
* Жанры:
  * Получение всех жанров: ```GET /api/v1/genres/```
  * Создание жанра: ```POST /api/v1/genres/``` (только для администратора)
  * Удаление жанра: ```DELETE /api/v1/genres/{slug}/``` (только для администратора)
* Произведения:
  * Получение списка произведений: ```GET /api/v1/titles/```
  * Создание произведения: ```POST /api/v1/titles/``` (только для администратора)
  * Частичное обновление произведения: ```PATCH /api/v1/titles/{title_id}/``` (только для администратора)
  * Удаление произведения: ```DELETE /api/v1/titles/{title_id}/``` (только для администратора)
* Отзывы:
  * Получение всех отзывов к произведению: ```GET /api/v1/titles/{title_id}/reviews/```
  * Создание отзыва: ```POST /api/v1/titles/{title_id}/reviews/``` (для аутентифицированных пользователей)
  * Получение отзыва по ID: ```GET /api/v1/titles/{title_id}/reviews/{review_id}/```
  * Частичное обновление отзыва: ```PATCH /api/v1/titles/{title_id}/reviews/{review_id}/``` (для автора, модератора или администратора)
  * Удаление отзыва: ```DELETE /api/v1/titles/{title_id}/reviews/{review_id}/``` (для автора, модератора или администратора)
* Комментарии к отзывам:
  * Получение всех комментариев к отзыву: ```GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/```
  * Создание комментария к отзыву: ```POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/``` (для аутентифицированных пользователей)
  * Получение комментария по ID: ```GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```
  * Частичное обновление комментария: ```PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/``` (для автора, модератора или администратора)
  * Удаление комментария: ```DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```  (для автора, модератора или администратора)
* Пользователи:
  * Получение списка пользователей: ```GET /api/v1/users/``` (для администратора)
  * Добавление пользователя: ```POST /api/v1/users/``` (для администратора)
  * Получение пользователя по username: ```GET /api/v1/users/{username}/``` (для администратора)
  * Изменение данных пользователя: ```PATCH /api/v1/users/{username}/```
  * Удаление пользователя: ```DELETE /api/v1/users/{username}/``` (для администратора)
  * Получение данных своей учетной записи: ```GET /api/v1/users/me/``` (для любого авторизованного пользователя)
  * Изменение данных своей учетной записи: ```PATCH /api/v1/users/me/``` (для любого авторизованного пользователя)
 
## Тестирование

Опишите, как запустить тесты:
```bash
python manage.py test
```

## Кон Contributors

- Имя - [Ваш GitHub](https://github.com/ваш-логин)

## Лицензия
