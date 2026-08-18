
# Инструкция по развёртыванию и запуску проекта. 


## Бэкенд

1. Зарегистрируйтесь или войдите в свой аккаунт на сайте REG.RU.
2. Создаём сервер (Ubuntu), выбираем тариф. Запоминаем (копируем) плавающий IP. 
3. В командной строке (терминал):
   
ssh root@...... (вводим IP)
   
5. Создаём нового пользователя и наделяет его правами. 

adduser user_name (вместо user_name вводим имя нового пользователя)
usermod user_name -aG sudo
sudo -i -u user_name (переключаемся на пользователя)

6. Обновляем установленные пакеты.

sudo apt update -y && apt upgrade -y

sudo apt-get install python3 python3-venv python3-pip postgresql nginx

7. Склонируйте в корень папки вашего пользователя репозиторий с проектом,
настройте виртуальное окружение Python и установите пакеты.

git clone ........ (вводим адрес репозитория)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip freeze (проверка установки модулей)

8. Создаём базу данных и суперпользователя.

sudo su postgres
psql
create user olga with superuser;
alter user postgres with password '123Qweasd~'

alter user olga with password '123Qweasd~'; 
create database mycloud;
\q
exit


9.  Делаем миграции.

python manage.py migrate

10. Собираем статику.

python manage.py collectstatic

11. В файле .env в папке frontend:

nano .env

VITE_API_URL=http://............/ (вводим IP)

12.  В командной строке (терминал), находясь в папке frontend:

sudo apt install npm

npm i

npm run build (осуществляем сборку)

13. Устанавливаем и настраиваем gunicorn.

pip install gunicorn

pip install django-cors-headers
В Setting.py меняем IP адрес
CORS_ALLOWED_ORIGINS = [
    "http://89.104.71.118:8000",
]
