# Distribution-API
### 1) Клонирум файлы ветки master данного репозитория в папку своего локального компьютера
`git clone https://github.com/amorid7956/distribution_project.git`
### 2) Заходим в папку проекта:
`cd distribution_project`
### 3) Запускаем контейнеры с redis и postgres:13(В отдельном окне терминала):
`docker-compose up --build`
### 4) Создаём виртуальное окружение(Note: для python 2.7):
`virtualenv -p /usr/bin/python2.7 venv`
### 5) Активируем виртуальное окружение:
`source venv/bin/activate`
### 6) Теперь, устанавливаем зависимости в ВО:
`pip install -r requirements.txt`
### 7) Так как файлы миграций уже созданы, то необходимости в makemigrations - нет, и выполняем команду.
`manage.py migrate`
### 8) Создаём суперпользователя:
`manage.py createsuperuser`
### 9) Запускаем воркера для выполнения celery задач(В отдельном окне терминала):
`celery --app distribution_project worker --loglevel=debug --concurrency=4`
### 10) Запускаем отслеживание периодических задач celery(В отдельном окне терминала):
`celery -A distribution_project beat -l info`
### 11) Запускаем отладочный сервер(В отдельном окне терминала):
`manage.py runserver`
