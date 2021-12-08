## Lab_3: Вступ до моніторингу.
1. Створоврюємо папку з назвою лабораторної роботи у власному репозиторію. Ініціалізуємо середовище `pipenv`, встановлюємо необхідні пакети та перевіряємо правильність встановлення за допомогою:
    ```bash
    sudo pipenv --python 3.8
    sudo pipenv install django
    django-admin --version
    ```
2. За допомогою Django Framework створюємо заготовку (template) `sudo pipenv run django-admin startproject my_site`
3. Запускаємо Django сервер. Переходимо на localhost:8000 командою : 
    `sudo pipenv run python manage.py runserver`
4. Зупиняємо сервер виконавши переривання `Ctrl+C`. Робимо коміт із базовим темплейтом сайту.
5. Далі робимо темплейт додатку у якому буде описано всі web сторінки сайту.:
    ` pipenv run python manage.py startapp main`
6. Робимо папку `main/templates/`, а також у даній папці файл з розширенням `.html` (`main.html`). Також у папці додатку робимо ще один файл `main/urls.py`. 
    
7. Після створення додатку нам потрібно вказати Django frameworks його назву та де шукати веб сторінки.
   Доданий вміст до файлу `my_site/settings.py`:
   ```bash
        INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'main'
    ], 
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('main.urls')),
    ]
    ```
   Доданий вміст до файлу `my_site/urls.py`:
    ```bash
   """my_site URL Configuration
    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/3.2/topics/http/urls/
    Examples:
    Function views
        Add an import:  from my_app import views
        Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        Add an import:  from other_app.views import Home
        Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
   Including another URLconf
        Import the include() function: from django.urls import include, path
        Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
   """
   from django.contrib import admin
   from django.urls import path, include
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('main.urls')),
   ]
   ```
8. Далі переходимо до нашого додатку та займемся WEB сторінками. Для цього: створимо сторінки двох типів - перша буде зчитуватись з `.html` темплейта. 
   друга сторінка буде просто повертати відповідь у форматі JSON;  відкрийемо та ознайомимось із вмістом файла `main/views.py`.
   Вміст файла `main/views.py`:
    ```bash
     from django.shortcuts import render
    from django.http import JsonResponse
    import os
    from datetime import datetime
    def main(request):
    return render(request, 'main.html', {'parameter': "test"})
    def health(request):
    response = {'date': 'test1', 'current_page': "test2", 'server_info': "test3", 'client_info': "test4"}
    return JsonResponse(response)
    ```
9. Щоб поєднати функції із реальними URL шляхами за якими будуть доступні наші веб сторінки заповнюємо файл `main/urls.py` Як можна зрозуміти з коду у нас є два URL посидання:
      - головна сторінка яка буде опрацьовуватись функцією `main`;
      - сторінка health/ яка буде опрацьована функцією `health`;
    ```bash
    from django.urls import path
    from . import views
    urlpatterns = [
    path('', views.main, name='main'),
    path('health/', views.health, name='health')
    ]
    ```
10. Запускаємо сервер та переконуємося що сторінки доступні. Робимо коміт робочого Django сайту.
    ```bash
    vlad@vlad-VirtualBox:~/stady/labs/Lab3$ sudo pipenv run python manage.py runserver
    Watching for file changes with StatReloader
    Performing system checks...
    
    System check identified no issues (0 silenced).
    
    You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    November 09, 2021 - 03:50:09
    Django version 3.2.9, using settings 'my_site.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    [09/Nov/2021 03:51:02] "GET / HTTP/1.1" 200 123
    ^Cvlad@vlad-VirtualBox:~/stady/labs/Lab3$
    ```
11. Роль моніторингу буде здійснювати файл `monitoring.py` який за допомогою бібліотеки `requests` буде опитувати сторінку `health`. Встановлюємо дану бібліотеку;
     `pipenv install requests`
12. Як видно із заготовленої функції health() відповідь формується як Пайтон словник і далі обробляється функцією JsonResponse(). 

13. Здача/захист лабораторної:
     1. модифікувати функцію `health` так щоб у відповіді були: згенерована на сервері дата, URL сторінки моніторингу, інформація про сервер на якому запущений сайт та інформація про клієнта який робить запит до сервера;
     2. дописати функціонал який буде виводити повідомлення про недоступність сайту у випадку якщо WEB сторінка недоступна
    Вміст створеного файлика `monitoring.py`:
    ```bash
    import requests
    import json
    import logging
    
    logging.basicConfig(
    filename="server.log",
    filemode='a',
    level=logging.INFO,
    format='{levelname} {asctime} {name} : {message}',
    style='{'
    )
    log = logging.getLogger(__name__)
    
    
    def main(url):
    try:
    r = requests.get(url)
    except Exception as x:
    logging.error("Сервер недоступний.")
    else:
    data = json.loads(r.content)
    logging.info("Сервер доступний. Час на сервері: %s", data['date'])
    logging.info("Запитувана сторінка: : %s", data['current_page'])
    logging.info("Відповідь сервера місти наступні поля:")
    for key in data.keys():
    logging.info("Ключ: %s, Значення: %s", key, data[key])
    if __name__ == '__main__':
    main("http://localhost:8000/health")
     ``` 
     3. після запуску моніторингу запит йде лише один раз після чого програма закінчується - зробіть так щоб дана програма запускалась раз в хвилину та працювала в бекграунді (період запуску зробити через функціонал мови Python);
    ```bash
    if __name__ == '__main__':
    while(True):
    main("http://localhost:8000/health")
    time.sleep(60)
     ```
     4. спростіть роботу з пайтон середовищем через швидкий виклик довгих команд, для цього зверніть увагу на секцію `scripts` у `Pipfile`. Зробіть аліас на запус моніторингу:
         `pipenv run mon`
        ```bash
        [scripts]
        server = "python manage.py runserver 0.0.0.0:8000"
        mon = "python3 monitoring.py"
        ```
14. Переконуємося що все працює, комітимо `server.logs` . 

15. Після успішного виконання роботи редагуємо  _README.md_ у цьому репозиторію.