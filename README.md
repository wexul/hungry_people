# Hungry People

Полнофункциональный сайт ресторана на Django.

Проект включает адаптивный лендинг, регистрацию и авторизацию пользователей, восстановление пароля, бронирование столиков, форму обратной связи и управление контентом через Django Admin.

## Возможности

### Пользовательская часть

- адаптивная одностраничная верстка;
- фиксированная шапка и мобильное меню;
- фильтрация блюд по категориям;
- галерея, слайдер и Яндекс Карта;
- регистрация, вход и выход без перезагрузки;
- восстановление пароля через email;
- бронирование столиков;
- форма обратной связи.

### Серверная часть

- Django Authentication и сессии;
- серверная валидация форм;
- хранение пользователей, бронирований и сообщений в базе данных;
- отправка писем о бронировании;
- восстановление пароля по email;
- управление контентом через Django Admin;
- поддержка SQLite и MySQL;
- хранение настроек в `.env`.

## Стек

- Python 3.11;
- Django 5.2.1;
- SQLite / MySQL;
- HTML, CSS, JavaScript;
- jQuery;
- Slick Carousel;
- Bootstrap.

## Установка

Команды предназначены для Git Bash на Windows.

### 1. Клонирование проекта

```bash
git clone https://github.com/wexul/hungry_people.git
cd hungry_people
```

### 2. Виртуальное окружение

```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Установка зависимостей

```bash
python -m pip install -r requirements.txt
```

### 4. Настройка `.env`

Создайте файл `.env` на основе примера:

```bash
cp .env.example .env
```

Минимальные настройки для SQLite:

```env
DJANGO_SECRET_KEY=вставьте-секретный-ключ
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
TIME_ZONE=Europe/London

DB_ENGINE=sqlite

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=Hungry People <noreply@example.com>
BOOKING_NOTIFICATION_EMAIL=your-email@example.com
```

Сгенерировать секретный ключ:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Подготовка базы данных

```bash
python manage.py migrate
```

Миграции создадут таблицы и добавят начальный контент сайта.

### 6. Создание администратора

```bash
python manage.py createsuperuser
```

### 7. Запуск

```bash
python manage.py runserver
```

Сайт:

```text
http://127.0.0.1:8000/
```

Административная панель:

```text
http://127.0.0.1:8000/admin/
```

## Настройка почты

По умолчанию используется консольный режим:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

В этом режиме письма выводятся в терминал и не отправляются на настоящий адрес.

Для отправки через Mail.ru создайте пароль для внешнего приложения и укажите в `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=465
EMAIL_HOST_USER=your-address@mail.ru
EMAIL_HOST_PASSWORD=пароль-внешнего-приложения

EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_TIMEOUT=20

DEFAULT_FROM_EMAIL=Hungry People <your-address@mail.ru>
BOOKING_NOTIFICATION_EMAIL=your-address@mail.ru
```

После изменения `.env` перезапустите сервер.
