# **Лабораторна робота №5**
---
## Послідовність виконання лабораторної роботи:
#### 1. Для ознайомляння з `docker-compose` звернувся до документації.
Щоб встановити `docker-compose` використав команди:
```text
 sudo apt-get docker-compose
```
#### 2. Ознайомився з бібліотекою `Flask`, яку найчастіше використовують для створення простих веб-сайтів на Python.
#### 3. Моє завдання: за допомогою Docker автоматизувати розгортання веб сайту з усіма супутніми процесами. Зроблю я це двома методами: 
* за допомогою `Makefile`;
* за допомогою `docker-compose.yaml`.

#### 4. Першим розгляну метод з `Makefile`, але спочатку створю робочий проект.
#### 5. Створив папку `my_app` в якій буде знаходитись мій проект. Створив папку `tests` де будуть тести на перевірку працездатності мого проекту. Скопіював файли `my_app/templates/index.html`, `my_app/app.py `, `my_app/requirements.txt`, `tests/conftest.py`, `tests/requirements.txt`, `tests/test_app.py` з репозиторію викладача у відповідні папки мого репозеторію. Ознайомився із вмістом кожного з файлів. Звернув увагу на файл requirements.txt у папці проекту та тестах. Даний файл буде мітити залежності для мого проекту він містить назви бібліотек які імпортуються.
#### 6. Я спробував чи проект є працездатним перейшовши у папку `my_app` та після ініціалізації середовища виконав команди записані нижче:
```text
sudo pipenv --python 3.8
sudo pipenv install -r requirements.txt
sudo pipenv run python app.py
```
1. Так само я ініціалузував середовище для тестів у іншій вкладці шелу та запустив їх командою `sudo pipenv run pytest test_app.py --url http://localhost:5000` але спочатку треба перейти в папку `tests`:
    ```text
    ============================= test session starts ==============================
    platform linux -- Python 3.9.5, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
    rootdir: /home/vlad/labs/lab5/tests
    collected 4 items                                                            
    
    test_app.py ..FF                                                         [100%]
    
    =================================== FAILURES ===================================
    __________________________________ test_logs ___________________________________

    url = 'http://localhost:5000'
    
        def test_logs(url):
            response = requests.get(url + '/logs')
    >       assert 'My Hostname is:' in response.text, 'Logs do not have Hostname'
    E       AssertionError: Logs do not have Hostname
    E       assert 'My Hostname is:' in '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...en(\'logs/app.log\', \'r\') as log:\nFileNotFoundError: [Errno 2] No such file or directory: \'logs/app.log\'\n\n-->\n'
    E        +  where '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...en(\'logs/app.log\', \'r\') as log:\nFileNotFoundError: [Errno 2] No such file or directory: \'logs/app.log\'\n\n-->\n' = <Response [500]>.text
    
    test_app.py:27: AssertionError
    ________________________________ test_main_page ________________________________
    
    url = 'http://localhost:5000'
    
        def test_main_page(url):
            response = requests.get(url)
    >       assert 'You are at main page.' in response.text, 'Main page without text'
    E       AssertionError: Main page without text
    E       assert 'You are at main page.' in '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...)\nredis.exceptions.ConnectionError: Error -3 connecting to redis:6379. Temporary failure in name resolution.\n\n-->\n'
    E        +  where '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...)\nredis.exceptions.ConnectionError: Error -3 connecting to redis:6379. Temporary failure in name resolution.\n\n-->\n' = <Response [500]>.text
    
    test_app.py:32: AssertionError
    =========================== short test summary info ============================
    FAILED test_app.py::test_logs - AssertionError: Logs do not have Hostname
    FAILED test_app.py::test_main_page - AssertionError: Main page without text
    ========================= 2 failed, 2 passed in 0.48s ==========================
    ```
2. Звернув увагу, що в мене автоматично створюються файли `Pipfile` та `Pipfile.lock`, а також на хост машині буде створена папка `.venv`. Після зупинки проекту видалив їх.
3. Перевірив роботу сайту перейшовши головну сторінку.

#### 7. Видалив файли які постворювались після тестового запуску. Щоб моє середовище було чистим, все буде створюватись і виконуватись всередині Docker. Створив два файла `Dockerfile.app`, `Dockerfile.tests` та `Makefile` який допоможе автоматизувати процес розгортання.
#### 8. Скопіював вміст файлів `Dockerfile.app`, `Dockerfile.tests` та `Makefile` з репозиторію викладача та ознайомився із вмістом `Dockerfile` та `Makefile` та його директивами. 
Вміст файла `Dockerfile.app`:
```text
FROM python:3.7-alpine
LABEL author="Vlad"

# оновлюємо систему та встановлюємо потрібні пакети
RUN apk update \
    && apk upgrade \
    && apk add git \
    && pip install pipenv

WORKDIR /app

# Копіюємо файл із списком пакетів які нам потрібно інсталювати
COPY my_app/requirements.txt ./
RUN pipenv install -r requirements.txt

# Копіюємо наш додаток
COPY my_app/ ./

# Створюємо папку для логів
RUN mkdir logs

EXPOSE 5000

ENTRYPOINT pipenv run python app.py
```
Вміст файла `Dockerfile.tests`:
```text
FROM python:3.7-alpine
LABEL author="Vlad"

# оновлюємо систему та встановлюємо потрібні пакети
RUN apk update \
    && apk upgrade \
    && apk add git \
    && pip install pipenv

WORKDIR /tests

# Копіюємо файл із списком пакетів які нам потрібно інсталювати
COPY tests/requirements.txt ./
RUN pipenv install -r requirements.txt

# Копіюємо нашого проекту
COPY tests/ ./

ENTRYPOINT pipenv run pytest test_app.py --url http://app:5000
```
Вміст файла `Makefile`:
```text
STATES := app tests
REPO := servaretur/lab5

.PHONY: $(STATES)

$(STATES):
	@docker build -f Dockerfile.$(@) -t $(REPO):$(@) .

run:
	@docker network create --driver=bridge appnet \
	&& docker run --rm --name redis --net=appnet -d redis \
	&& docker run --rm --name app --net=appnet -p 5000:5000 -d $(REPO):app

test-app:
	@docker run --rm -it --name test --net=appnet $(REPO):tests

docker-prune:
	@docker rm $$(docker ps -a -q) --force || true \
	&& docker container prune --force \
	&& docker volume prune --force \
	&& docker network prune --force \
	&& docker image prune --force
removeImages:
	@docker rmi $$(docker images -q) --force
PushToDocker:
	@docker login \
	&& docker push $(REPO):app \
	&& docker push $(REPO):tests
```
Дерективи `app` та `tests`:
Створення імеджів для сайту та тесту.
Деректива `run`:
Запускає сайт.
Деректива `test-app`:
Запуск тесту.
Деректива `docker-prune`:
Очищення іміджів.
#### 9. Для початку, використовуючи команду `sudo make app` створив Docker імеджі для додатку та для тестів `sudo make tests`. Теги для цих імеджів є з моїм Docker Hub репозиторієм. Запустив додаток командою `sudo make run` та перейшовши в іншу вкладку шелу запустіть тести командою `sudo make test-app`.
Запуск сайту
```text
vlad@vlad-VirtualBox:~/labs/lab5$ sudo make run
[sudo] password for vlad: 
5a59f988768827aa44e7b5e9904e4f3d2692ffd1bf8c78e262fd16d87790717b
Unable to find image 'redis:latest' locally
latest: Pulling from library/redis
eff15d958d66: Pull complete 
1aca8391092b: Pull complete 
06e460b3ba1b: Pull complete 
def49df025c0: Pull complete 
646c72a19e83: Pull complete 
db2c789841df: Pull complete 
Digest: sha256:619af14d3a95c30759a1978da1b2ce375504f1af70ff9eea2a8e35febc45d747
Status: Downloaded newer image for redis:latest
5d3c4e343ac11e52d0e53cc314d99b224a14dfc0d0361ee3c24b2c55e5f0e903
3e719efd34012a377571a3207e660531d1f6b18164e7bbb5bc144b847787c476
```
Проходження тесту:
```text
vlad@vlad-VirtualBox:~/labs/lab5$ sudo make test-app
Warning: Your Pipfile requires python_version 3.9, but you are using 3.8.12 (/root/.local/share/v/t/bin/python).
  $ pipenv --rm and rebuilding the virtual environment may resolve the issue.
  $ pipenv check will surely fail.
============================= test session starts ==============================
platform linux -- Python 3.8.12, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /tests
collected 4 items                                                              

test_app.py ....                                                         [100%]

============================== 4 passed in 0.24s ===============================
vlad@vlad-VirtualBox:~/labs/lab5$
```
#### 10. Зупинив проект натиснувши Ctrl+C та почистив всі ресурси `Docker` за допомогою `make`.
```text
vlad@vlad-VirtualBox:~/labs/lab5$ sudo make docker-prune
[sudo] password for vlad: 
3e719efd3401
5d3c4e343ac1
3044d4300891
ab8221ccae28
8afa1cc22d03
7d38d9594c2e
3282dc276687
bfd0bd0bcee8
Total reclaimed space: 0B
Deleted Volumes:
7f09c2bd964c9c17e7a1433e63435de02a2215081acba88d51167ef905e54265

Total reclaimed space: 0B
Deleted Networks:
appnet

Total reclaimed space: 0B
vlad@vlad-VirtualBox:~/labs/lab5$
```

#### 11. Створив директиву `PushToDocker` в Makefile для завантаження створених імеджів у мій Docker Hub репозиторій.
Деректива `docker-push`:
```text
PushToDocker:
	@docker login \
	&& docker push $(REPO):app \
	&& docker push $(REPO):tests
```

#### 12. Видалив створені та закачані імеджі. Команда `docker images` виводить пусті рядки. Створив директиву в Makefile яка автоматизує процес видалення моїх імеджів.
Деректива `removeImages`:
```text
removeImages:
	@docker rmi $$(docker images -q) --force
```

#### 13. Перейшов до іншого варіанту з використанням `docker-compose.yaml`. Для цього створив даний файл у кореновій папці проекту та заповнив вмістом з прикладу. Проект який я буду розгортити за цим варіантом трохи відрізняється від першого тим що у нього зявляється дві мережі: приватна і публічна.
Файл `docker-compose.yaml`:
```text
version: '3.7'
services:
  hits:
    build:
      context: .
      dockerfile: Dockerfile.app
    image: servaretur/lab5:compose-app
    container_name: app
    depends_on:
      - redis
    networks:
      - public
      - secret
    ports:
      - 80:5000
    volumes:
      - hits-logs:/hits/logs
  tests:
    build:
      context: .
      dockerfile: Dockerfile.tests
    image: servaretur/lab5:compose-tests
    container_name: tests
    depends_on:
      - hits
    networks:
      - public
  redis:
    image: redis:alpine
    container_name: redis
    volumes:
      - redis-data:/data
    networks:
      - secret
volumes:
  redis-data:
    driver: local
  hits-logs:
    driver: local

networks:
  secret:
    driver: bridge
  public:
    driver: bridge
```

#### 14. Перевірив чи `Docker-compose` встановлений та працює у моїй системі, а далі просто запускаю `docker-compose`:
```text
docker-compose --version
sudo docker-compose -p lab5 up
```
```text
vlad@vlad-VirtualBox:~/labs/lab5$ docker-compose --version
docker-compose version 1.25.0, build unknown
vlad@vlad-VirtualBox:~/labs/lab5$
```

#### 15. Перевірив чи працює веб-сайт. Дана сторінка відображається за адресою `http://172.19.0.2:5000/`:
#### 16. Перевірив чи компоуз створив докер імеджі. Всі теги коректні і назва репозиторія вказана коректно:
```text
vlad@vlad-VirtualBox:~/labs/lab5$ sudo docker images
[sudo] password for vlad: 
REPOSITORY          TAG             IMAGE ID       CREATED          SIZE
servaretur/lab5   compose-tests   9db98127b13e   20 minutes ago   301MB
servaretur/lab5   compose-app     94499c320c52   22 minutes ago   299MB
python              3.7-slim        64458f531a7e   6 days ago       122MB
redis               alpine          5c08f13a2b92   10 days ago      32.4MB
```

#### 17. Зупинив проект натиснувши `Ctrl+C` і почистітив ресурси створені компоуз командою `docker-compose down`.

#### 18. Завантажив створені імеджі до Docker Hub репозиторію за допомого команди `sudo docker-compose push`.

#### 19. Що на Вашу думку краще використовувати `Makefile` чи `docker-compose.yaml`? - На мою думку через `docker-compose.yaml` набагато швидше і простіше

#### 20. (Завдання) Оскільки Ви навчились створювати docker-compose.yaml у цій лабораторній то потрібно:
- Cтворив `docker-compose.yaml` для лабораторної №4. Компоуз повинен створити два імеджі для `Django` сайту та моніторингу, а також їх успішно запустити.
Файлик `docker-compose.yaml`:
```text
version: '3.7'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    image: servaretur/lab4:compose-app
    container_name: app
    networks:
      - public
    ports:
      - 8000:8000
  monitoring:
    build:
      context: .
      dockerfile: Dockerfile.site
    image: servaretur/lab4:compose-monitoring
    container_name: monitoring
    network_mode: host
      
networks:
  public:
    driver: bridge
```
#### 21. Після успішного виконання роботи я відредагував свій `README.md` у цьому репозиторію та створив pull request.
