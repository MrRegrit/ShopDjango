![Pipeline Status](https://gitlab.crja72.ru/django_2023/students/142182-renatgaboff-course-967/badges/main/pipeline.svg)

## Технологии
- Python 3.11
- Django 4.2

## Диаграмма Базы Данных
![DataBase](ER.jpg)

# Установка 
## Клонирование репозитория
```
git clone https://gitlab.crja72.ru/django_2023/students/142182-renatgaboff-course-967.git
```
## Создание виртуального окружения
### Для Linux
```
python3 -m venv venv
source venv/bin/activate
```
### Для Windows
```
python -m venv venv
venv\bin\activate
```
## Установка .env
### Для Linux
```
mv template.env .env
```
И измените .env под себя
### Для Windows
```
ren template.env .env
```
И измените .env под себя

## Установка requirements
### Выберите один из файлов
Для работы сайта:
```
pip install -r requirements/prod.txt
```
Для разработки:
```
pip install -r requirements/dev.txt
```
Для тестирования и отладки:
```
pip install -r requirements/test.txt
```

## Перейдите в директорию lyceum
```
cd lyceum
```

## Создание локализации
```
django-admin makemessages -l ru
django-admin makemessages -l en
django-admin compilemessages
```

# Запуск проекта
```
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures/data.json
python manage.py runserver
```
