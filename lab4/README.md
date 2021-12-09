# **Лабораторна робота №4**
---
## Послідовність виконання лабораторної роботи:
#### 1. Ознайомився з документацією `Docker`.
#### 2. Для перевірки чи докер встановлений і працює правильно на віртуальній машині запустітив перевірку версії командою `sudo docker -v > my_work.log`, виведення допомоги командою `sudo docker --help >> my_work.log` та тестовий імедж командою `sudo docker run docker/whalesay cowsay Docker is fun >> my_work.log`. Вивід цих команд перенаправляв у файл `my_work.log` та закомітив його до репозиторію.
#### 3. `Docker` працює з Імеджами та Контейнерами. Імедж це свого роду операційна система з попередньо інстальованим ПЗ. Контейнер це запущений Імедж. Ідея роботи `Docker` дещо схожа на віртуальні машини. Спочатку створив імедж з якого буде запускатись контейнер.
#### 4. Для знайомства з `Docker` створив імедж із `Django` сайтом зробленим у попередній роботі.
1. ##### Оскільки мій проект на `Python` то і базовий імедж також потрібно вибрати відповідний. Використовую команду `docker pull python:3.8-slim` щоб завантажити базовий імедж з репозиторію. Переглядаю створеного вміст імеджа командою `docker inspect python:3.8-slim`
    ##### Перевіряю чи добре встановився даний імедж командою:
    
```text
vlad@vlad-VirtualBox:~$ sudo docker images
[sudo] пароль для vlad: 
REPOSITORY        TAG          IMAGE ID       CREATED          SIZE
python            3.8-slim     1e46b5746c7c   6 days ago       122MB
hello-world       latest       feb5d9fea6a5   2 months ago     13.3kB
docker/whalesay   latest       6b362a9f73eb   6 years ago      247MB
vlad@vlad-VirtualBox:~$
```

2. ##### Створив файл з іменем `Dockerfile` та скопіював туди вміс такого ж файлу з репозиторію викладача.
    ###### Вміст файлу `Dockerfile`:
    ```text
    FROM python:3.8-slim
    
    LABEL author="Bohdan"
    LABEL version=1.0
    
    # оновлюємо систему
    RUN apt-get update && apt-get upgrade -y
    
    # Встановлюємо потрібні пакети
    RUN apt-get install git -y && pip install pipenv
    
    # Створюємо робочу папку
    WORKDIR /lab
    
    # Завантажуємо файли з Git
    RUN git clone https://github.com/BobasB/devops_course.git
    
    # Створюємо остаточну робочу папку з Веб-сайтом та копіюємо туди файли
    WORKDIR /app
    RUN cp -r /lab/devops_course/lab3/* .
    
    # Інсталюємо всі залежності
    RUN pipenv install
    
    # Відкриваємо порт 8000 на зовні
    EXPOSE 8000
    
    # Це команда яка виконається при створенні контейнера
    ENTRYPOINT ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
    ```
3. ##### Ознайомився із коментарями та зрозумів структуру написання `Dockerfile`.
4. ##### Змінений`Dockerfile` файл:
```text
FROM python:3.8-slim

LABEL author="Vlad"
LABEL version=1.0

# оновлюємо систему
RUN apt-get update && apt-get upgrade -y

# Встановлюємо потрібні пакети
RUN apt-get install git -y && pip install pipenv

# Створюємо робочу папку
WORKDIR /lab

# Завантажуємо файли з Git
RUN git clone https://github.com/VladyslavSembai/VladyslavSembai-IK-31.git

# Створюємо остаточну робочу папку з Веб-сайтом та копіюємо туди файли
WORKDIR /app
RUN cp -r /lab/VladyslavSembai-IK-31/lab3/* .

# Інсталюємо всі залежності
RUN pipenv install

# Відкриваємо порт 8000 на зовні
EXPOSE 8000

# Це команда яка виконається при створенні контейнера
ENTRYPOINT ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
```

#### 5. Створив власний репозиторій на [Docker Hub](https://cloud.docker.com/repository/registry-1.docker.io/vlad5841/lab4). Для цього залогінився у власний аккаунт на `Docker Hub` після чого перейшов у вкладку Repositories і далі натиснув кнопку `Create new repository`.
#### 6. Виконав білд (build) Docker імеджа та завантажтажив його до репозиторію. Для цього я повинен вказати правильну назву репозиторію та TAG. Оскільки мій репозиторій `vlad5841/lab4` то команда буде виглядати `sudo docker build -t vlad5841/lab4:django .`, де `django` - це тег.
Команда `docker images`:
```text
vlad@vlad-VirtualBox:~$ sudo docker images
[sudo] пароль для vlad: 
REPOSITORY        TAG          IMAGE ID       CREATED          SIZE
vlad5841/lab4     django       adbe22ba5a9b   48 minutes ago   331MB
vlad5841/lab4     monitoring   adbe22ba5a9b   48 minutes ago   331MB
<none>            <none>       a9add805bd68   52 minutes ago   266MB
python            3.8-slim     1e46b5746c7c   6 days ago       122MB
hello-world       latest       feb5d9fea6a5   2 months ago     13.3kB
docker/whalesay   latest       6b362a9f73eb   6 years ago      247MB
vlad@vlad-VirtualBox:~$
```
Команда щоб залогінитись `docker login -u "vlad5841" -p "**********" docker.io`
Команда для завантаження на власний репозеторій `docker push vlad5841/lab4:django`.
Посилання на мій [`Docker Hub`](https://cloud.docker.com/repository/registry-1.docker.io/vlad5841/lab4) репозиторій та посилання на [`імедж`](https://hub.docker.com/layers/181552450/vlad5841/lab4/django/images/sha256-2e0aadd7dc92dfc138d4926ede8513fdf38c3f7db1a1c69bdc472e9753f8b13d?context=repo).
#### 7. Для запуску веб-сайту виконав команду `sudo docker run -it --name=django --rm -p 8000:8000 baracuda794/lab4:django`:
```text
vlad@vlad-VirtualBox:~$ sudo docker run -it --name=django --rm -p 8000:8000 vlad5841/lab4:django
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
December 09, 2021 - 12:36:06
Django version 3.2.9, using settings 'my_site.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```
#### 8. Оскільки веб-сайт готовий і працює, потрібно створит ще один контейнер із програмою моніторингу нашого веб-сайту (Моє Завдання на роботу):
1. ##### Створив ще один Dockerfile з назвою `Dockerfile.site` в якому помістив програму моніторингу.
    Вміст файлу `Dockerfile.site`:
```text
FROM python:3.8-slim

LABEL author="Vlad"
LABEL version=1.0

# оновлюємо систему
RUN apt-get update && apt-get upgrade -y

# Встановлюємо потрібні пакети
RUN apt-get install git -y && pip install pipenv

# Створюємо робочу папку
WORKDIR /lab

# Завантажуємо файли з Git
RUN git clone https://github.com/VladyslavSembai/VladyslavSembai-IK-31.git

# Створюємо остаточну робочу папку з Веб-сайтом та копіюємо туди файли
WORKDIR /app
RUN cp -r /lab/VladyslavSembai-IK-31/lab3/* .

# Інсталюємо всі залежності
RUN pipenv install

# Відкриваємо порт 8000 на зовні
EXPOSE 8000

# Це команда яка виконається при створенні контейнера
ENTRYPOINT ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
```
2. ##### Виконав білд даного імеджа та дав йому тег `monitoring` командами:
    ```text
    sudo docker build -f Dockerfile.site -t vlad5841/lab4:monitoring .
    docker push vlad5841/lab4:monitoring
    ```
3. ##### Запустив два контейнери одночасно (у різних вкладках) та переконався що програма моніторингу успішно доступається до сторінок мого веб-сайту.
    ##### Використовуючи команди:
    Запуск серевера:
```text
vlad@vlad-VirtualBox:~$ sudo docker run -it --name=django --rm -p 8000:8000 vlad5841/lab4:django
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
December 09, 2021 - 12:36:06
Django version 3.2.9, using settings 'my_site.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
[05/Dec/2021 11:14:04] "GET /health HTTP/1.1" 301 0
[05/Dec/2021 11:14:04] "GET /health/ HTTP/1.1" 200 340
 
```

    Запуск моніторингу:
```text
    vlad@vlad-VirtualBox:~/tpis/Vladyslav_Sembai_IK-31/lab4$ sudo docker run -it --name=monitoring --rm --net=host -v $(pwd)/server.log:/app/server.log vlad5841/lab4:monitoring
    ^CTraceback (most recent call last):
      File "monitoring.py", line 32, in <module>
        time.sleep(60)
    KeyboardInterrupt
```
4. ##### Закомітив `Dockerfile.site` та результати роботи програми моніторингу запущеної з `Docker` контейнера.

