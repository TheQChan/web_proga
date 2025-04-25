# Kinoman

Kinoman - это современная веб-платформа для любителей кино, построенная на Django. Сайт позволяет пользователям просматривать информацию о фильмах, оставлять отзывы и оценки, а также взаимодействовать с другими киноманами.

## Функциональность

- Просмотр популярных и новых фильмов
- Детальная информация о каждом фильме
- Система рейтингов и комментариев
- Пользовательские профили
- Адаптивный дизайн
- Анимации и современный интерфейс

## Технологии

- Django 5.0.1
- Bootstrap 5
- Animate.css
- Font Awesome
- JavaScript (ES6+)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/kinoman.git
cd kinoman
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/Scripts/activate  # для Windows
source venv/bin/activate     # для Linux/Mac
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта

```
kinoman/
├── media/          # Загруженные медиафайлы
│   ├── avatars/    # Аватары пользователей
│   └── posters/    # Постеры фильмов
├── static/         # Статические файлы
│   ├── css/        # Стили
│   ├── js/         # JavaScript
│   └── img/        # Изображения
├── templates/      # HTML шаблоны
├── movies/         # Основное приложение
└── kinoman/        # Настройки проекта
```

## Лицензия

MIT License 