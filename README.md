# YaCut
YaCut - сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис. 

## Установка
Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```
Создать и заполнить файл `.env` переменными окружения

```bash
touch .env
# Имя приложения (название директории с Flask-приложением)
echo "FLASK_APP=yacut" >> .env
# Режим отладки: 1—включено, 0—выключено. Не используйте отладку в продакшене!
echo "FLASK_DEBUG=0" >> .env
# Конфигурация базы данных: создаст db.sqlite3 в папке ./instance
# Используйте любую базу данных, поддерживаемую Flask-SQLAlchemy
echo "SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3" >> .env
# Генерация секретного ключа
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" >> .env
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
## Запуск
```bash
flask run
```
## Примеры запросов к API
Для удобной работы с API воспользуйтесь онлайн-редактором 
[Swagger Editor](https://editor.swagger.io/), 
в котором можно визуализировать спецификацию `./openapi.yml`

## Контакты
**Автор:** Ходорищенко Валерий (Khodorishchenko Valeriy)

[![GitHub](https://img.shields.io/badge/GitHub-%23000000?style=flat&logo=github&logoColor=white)](https://github.com/Valerii-Khodorishchenko)
[![Telegram](https://img.shields.io/badge/Telegram-%2300A9E0?style=flat&logo=telegram&logoColor=white)](https://t.me/KhodorishchenkoValerii)