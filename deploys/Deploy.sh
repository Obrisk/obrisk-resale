# These are the list of commands on how to deploy obrisk on a fresh Ubuntu 18.04 OS running on AWS Lightsail.
sudo apt-get update
sudo apt-get -y upgrade

sudo apt install python3-pip python3-dev libpq-dev nginx curl redis-server -y
#sudo apt install postgresql if you will want to access DB with psql
sudo vim /etc/redis/redis.conf #Then change line 147 from 'supervised no' to 'supervised systemd'
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

sudo mkdir /tmp/logs
sudo chmod 664 -R /tmp/logs
sudo touch /tmp/logs/gunicorn-access.log /tmp/logs/gunicorn-error.log /tmp/logs/nginx-access.log /tmp/logs/nginx-error.log 


sudo cp deploys/gunicorn.socket /etc/systemd/system
sudo cp deploys/gunicorn.service /etc/systemd/system
sudo cp deploys/uvicorn.socket /etc/systemd/system
sudo cp deploys/uvicorn.service /etc/systemd/system

sudo systemctl start gunicorn.socket uvicorn.socket
sudo systemctl enable gunicorn.socket uvicorn.socket

curl --unix-socket /run/gunicorn.sock localhost #Not a must, just activate socket.
curl --unix-socket /run/uvicorn.sock localhost

sudo cp deploys/obrisk /etc/nginx/sites-available 
sudo ln -s /etc/nginx/sites-available/obrisk /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo ufw allow 22
sudo ufw enable -y

sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx -y

#If you want to change the IP of the server to a static one for quick provision
#then you have to logout the ssh mode before performing the next step.
#only after having the right IP for Obrisk.com the following can be valid
#When the IP of instance is changed reset the ssh by 
#ssh-keygen -R <the-ip-address> 
sudo certbot --nginx  #interactive step




























