#!/bin/bash -xe
# These are the list of commands on how to deploy obrisk on a fresh Ubuntu 18.04 OS running on AWS Lightsail.
# Some command requires raw password input and they can't be automated
# Examples are creating linux user, and github keys. In such cases raw values can be passed when script is started by someone
# sudo vim /etc/redis/redis.conf #Then change line 147 from 'supervised no' to 'supervised systemd'
# Also check for safe ways to inject .env in the middle of this script

#It is possible to store all passwords in a separate script that will echo them when runnning specific commands.
#https://serverfault.com/questions/815043/how-to-give-username-password-to-git-clone-in-a-script-but-not-store-credential
 

sudo apt-get -y update

#First, install codedeploy agent.
sudo apt-get -y install ruby
sudo apt-get -y install wget
cd /home/ubuntu
#wget https://bucket-name.s3.region-identifier.amazonaws.com/latest/install
wget https://aws-codedeploy-cn-northwest-1.s3.cn-northwest-1.amazonaws.com.cn/latest/install
chmod +x ./install
sudo ./install auto

sudo service codedeploy-agent start
sudo service codedeploy-agent status

echo 'alias python="python3.6"' >> ~/.bashrc
source ~/.bashrc

sudo apt install python3-venv gcc python3-pip python3-dev libpq-dev python3-wheel nginx curl redis-server npm -y

sudo -H pip3 install --upgrade pip wheel setuptools

sudo useradd -m -p "$(python -c "import crypt; print crypt.crypt(\"REPLACE-WITH-RAW-PS\", \"\$6\$$(</dev/urandom tr -dc 'a-zA-Z0-9' | head -c 32)\$\")")" -s /bin/bash obdev-user
sudo gpasswd -a obdev-user sudo
sudo su - obdev-user

#Beware of the space btn file name and -q to mean quiet
#Make sure the key is created as id_rsa the default name
ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N "" -C "REPLACE-WITH-EMAIL"

eval "$(ssh-agent -s)"
ssh-add -k ~/.ssh/id_rsa

RSA_KEY=$(cat ~/.ssh/id_rsa.pub)

curl -u "REPLACE-WITH-USERNAME:REPLACE-WITH-PS" --data '{"title":"EC2-instance<REPLACE-WITH-NUM>","key":"'"$RSA_KEY"'"}' https://api.github.com/user/keys

git clone git@github.com:elshaddae/obdev2018.git

#Create them here so that they are out of git VCS
mkdir ./logs ./run
chmod 764 -R ./logs ./run

touch ./logs/gunicorn-access.log ./logs/gunicorn-error.log ./logs/nginx-access.log ./logs/nginx-error.log ./logs/celery-access.log ./logs/celery-error.log
mkdir ./run/gunicorn ./run/uvicorn ./run/celery

cd obdev2018
#it turns out that I still can't access the virtual-env files inside vim.
#but  this behaviour is not required in production (so comment virualenv)
sudo -H pip3 install --upgrade pip
#sudo -H pip3 install virtualenv
#virtualenv venv_obrisk
cp utility/pip.conf ~/.pip/pip.conf

python -m venv venv_obrisk
source venv_obrisk/bin/activate

#It is not a guarantee that this process will pass smoothly
#Always when there is a failure update the req files and rerun the command.
pip install -r requirements/production.txt

#This step onwards needs the env variables loaded
#vim .env #Add all the settings parameters.

#THE SERVERS SHARE DB AND S3 STORAGE THIS SHOULDN'T BE RUN ON EVERY SERVER
#python manage.py migrate
#python manage.py collectstatic 
#static files on the local(static) to be served by Nginx for PWA features.
python manage.py collectstatic --settings=config.settings.static 

sudo cp deploys/gunicorn.socket /etc/systemd/system
sudo cp deploys/gunicorn.service /etc/systemd/system
sudo cp deploys/uvicorn.socket /etc/systemd/system
sudo cp deploys/uvicorn.service /etc/systemd/system
sudo cp deploys/gulp.service /etc/systemd/system
sudo cp deploys/celery.service /etc/systemd/system
sudo cp deploys/celerybeat.service /etc/systemd/system

sudo systemctl start gunicorn.socket uvicorn.socket
sudo systemctl enable gunicorn.socket uvicorn.socket

sudo cp deploys/obrisk /etc/nginx/sites-available 
sudo ln -s /etc/nginx/sites-available/obrisk /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo ufw allow 22
#sudo ufw enable -y

# Gulp should be run locally to help update the static files for Nginx root
# These files are called by service worker from / of Obrisk.com
cd ./frontend
sudo npm install cnpm -g
cnpm install
cnpm install gulp
sudo systemctl start gulp.service

/home/obdev-user/obdev2018/frontend/node_modules/gulp/bin/gulp.js build

#DONE!
#In case of errors check below commands 
#sudo systemctll status <service-name.service>
#journalctl -u <service-name.service>
#sudo systemctl restart gunicorn.service uvicorn.service celery.service celerybeat.service
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#These steps aren't used when spinning server behind NLB
#sudo add-apt-repository ppa:certbot/certbot
#sudo apt-get update
#sudo apt-get install python-certbot-nginx -y

#If you want to change the IP of the server to a static one for quick provision
#then you have to logout the ssh mode before performing the next step.
#only after having the right IP for Obrisk.com (54.180.169.125) the following can be valid
#When the IP of instance is changed reset the ssh by 
#ssh-keygen -R <the-ip-address> 
#sudo certbot --nginx  #interactive step

#To copy data from one db instance to another.
#pg_dump -C -h localhost -U obrisk -P obrisk_db | psql -h ls-475c8c9aa913ef145c97aecda604ec8b6ae7a92f.ccyq1xb49cwb.ap-northeast-2.rds.amazonaws.com -U dbobdevuser2018 obrisk_db



