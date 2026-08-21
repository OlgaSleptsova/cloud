
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



10.  В файле .env в папке frontend:

nano .env

VITE_API_URL=http://............/ (вводим IP)

11.  В командной строке (терминал), находясь в папке frontend:

sudo apt install npm

npm i

npm run build (осуществляем сборку)

12. Устанавливаем и настраиваем gunicorn.

pip install gunicorn
sudo nano /etc/systemd/system/gunicorn.service (создаем файл с настройками)
в файле делаем следующую запись:
[Unit]
Description=gunicorn service
After=network.target

[Service]
User=olga
Group=www-data
WorkingDirectory=/home/olga/cloud/mycloud
ExecStart=/home/olga/cloud/mycloud/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/olga/cloud/mycloud/mycloud/project.sock \
          mycloud.wsgi:application

[Install]
WantedBy=multi-user.target

запускаем сервер
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

13. Установливаем nginx.

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

    
sudo nano /etc/nginx/sites-available/mycloud (создаем файл с настройками)

Сделать запись в файле:
server {
        listen 80;
        server_name 89.108.71.67;

        location /static/ {
                root /home/olga/cloud/mycloud;
        }
        location / {
            include proxy_params;
            proxy_pass http://unix:/home/olga/cloud/mycloud/mycloud/project.sock;
            }
         
}

Переопределяем конфигурации сервера nginx и проверяем его работоспособность:

sudo systemctl reload nginx
sudo systemctl status nginx

14.  Собираем статику.

cd ~/cloud/mycloud
python manage.py collectstatic --noinput

15. Перезапускаем Gunicorn
    sudo systemctl restart gunicorn
    

