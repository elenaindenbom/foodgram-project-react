# Foodrgam

 Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект реализован на `Django` и `DjangoRestFramework`. Доступ к данным реализован через API-интерфейс.
Инструменты и стек: python, JSON, Django, React, Telegram, API, Docker, Nginx,
                    PostgreSQL, Gunicorn, JWT, Postman

## Особенности реализации

- Проект завернут в Docker-контейнеры;
- Образы foodgram_frontend и foodgram_backend запушены на DockerHub;
- Подключено SPA к бэкенду на Django через API;
- Реализован workflow c автодеплоем на удаленный сервер;
- Проект развернут на сервере: <http://51.250.6.43/recipes>


### Развертывание на локальном сервере

1. Установите на сервере `docker` и `docker-compose`.
2. Создайте файл `/infra/.env`.
3. Выполните команду `docker-compose up -d --buld`.
4. Выполните миграции `docker-compose exec backend python manage.py migrate`.
5. Создайте суперюзера `docker-compose exec backend python manage.py createsuperuser`.
6. Соберите статику `docker-compose exec backend python manage.py collectstatic --no-input`.
7. Заполните базу ингредиентами `docker-compose exec backend python manage.py load_ingredients`.
8. **Для корректного создания рецепта через фронт, надо создать пару тегов в базе через админку.**
9. Документация к API находится по адресу: <http://localhost/api/docs/redoc.html>.

## Автор

Инденбом Елена
