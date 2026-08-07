
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

8. Создаём базу данных.

sudo su postgres
psql
CREATE USER olga WiTH SUPERUSER;
CREATE USER vova WiTH SUPERUSER;
create user vova with superuser;
alter user olga with password '123Qweasd~' (вводим пароль);
alter user vova with password '123Qweasd~'; (вводим пароль);
alter user postgres with password '123Qweasd~' (вводим пароль);
create database mydatabase;
\q
exit


<!-- create database olga;
\q
exit
psql
create database mydatabase;
\q -->

9. Меняем настройки в Settings.py
nano mycloud/settings.py
ALLOWED_HOSTS = [] добавляем IP адрес сервера

10. Делаем миграции.

python manage.py migrate

10. Собираем статику.

python manage.py collectstatic

12. Устанавливаем и настраиваем gunicorn.

pip install gunicorn

Запускаем gunicorn, добавляем в автозагрузку и проверяем его работу:

sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

13. Установливаем nginx.

apt install nginx
sudo nano /etc/nginx/nginx.conf (меняем  ubuntu на имя вашего пользователя)

    user ......;
    worker_processes auto;
    pid /run/nginx.pid;
    error_log /var/log/nginx/error.log;
    include /etc/nginx/modules-enabled/*.conf;
    
    events {
            worker_connections 768;
            # multi_accept on;
    }
    
    http {
            sendfile on;
            tcp_nopush on;
            types_hash_max_size 2048;
           
            include /etc/nginx/mime.types;
            default_type application/octet-stream;
    
            ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
            ssl_prefer_server_ciphers on;
    
            access_log /var/log/nginx/access.log;
    
            gzip on;
            include /etc/nginx/conf.d/*.conf;
            include /etc/nginx/sites-enabled/*;
    }


sudo nano /etc/nginx/sites-available/default (далем настройку nginx, указываем IP)

    server {
        listen 80;
        server_name ........;

        root /var/www/html;
        index index.html;

        location / {
            try_files $uri /index.html;

        location /api {
                proxy_pass http://127.0.0.1:8000;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }    
        
        
        location /media/ {
                alias /home/anton/Mycloud/mycloud/media/;
        }

        location /static/ {
                alias /var/www/static/;
        }
    }


Переопределяем конфигурации сервера nginx и проверяем его работоспособность:

sudo systemctl reload nginx
sudo systemctl status nginx

14. Запускаем проект 'Mycloud'(находясь в директории /Mycloud/mycloud/).

gunicorn mycloud.wsgi -b 0.0.0.0:8000 (меняем в файле setting.py - DEBUG=Fals)
