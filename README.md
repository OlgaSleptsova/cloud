
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
create user olga with superuser;
alter user olga with password '123Qweasd~'; (вводим пароль);
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


