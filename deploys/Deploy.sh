# These are the list of commands on how to deploy obrisk on a fresh Ubuntu 18.04 OS running on AWS Lightsail.
sudo apt-get update
sudo apt-get -y upgrade

sudo apt install python3-pip python3-dev libpq-dev nginx curl redis-server -y
#sudo apt install postgresql if you will want to access DB with psql
sudo vim /etc/redis/redis.conf #Then change line 147 from 'supervised no' to supervised 'systemd'
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
sudo adduser obdev-user  #Interactive step
sudo gpasswd -a obdev-user sudo
sudo su - obdev-user

virtualenv venv_obrisk
source venv_obrisk/bin/activate
git clone https://github.com/elshaddae/obdev2018.git  #Psword required.
cd obdev2018
pip install -r requirements/production.txt
vim .env #Add all the settings parameters.
python manage.py migrate
python manage.py collectstatic --settings=config.settings.static #Pass the settings parameter only when django-storages is not working

sudo mkdir /home/obdev-user/logs /tmp/logs
sudo touch /home/obdev-user/logs/gunicorn-access.log /home/obdev-user/logs/gunicorn-error.log \
/home/obdev-user/logs/nginx-access.log /home/obdev-user/logs/nginx-error.log  

sudo cp deploys/gunicorn.socket /etc/systemd/system
sudo cp deploys/gunicorn.service /etc/systemd/system
sudo cp deploys/uvicorn.socket /etc/systemd/system
sudo cp deploys/uvicorn.service /etc/systemd/system

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl start uvicorn.socket
sudo systemctl enable uvicorn.socket



















