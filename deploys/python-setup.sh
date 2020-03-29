#!/bin/bash

source venv_obrisk/bin/activate
pip install -r requirements/production.txt

cd ./frontend
/home/ubuntu/obdev2018/frontend/node_modules/gulp/bin/gulp.js build
cd ..

#Only migrate and collectstatic on one instance
EC2_INSTANCE_ID=$(ec2metadata --instance-id)

if [ "$EC2_INSTANCE_ID" = "i-09290a52964419c47" ]; then
    echo "This is instance-1"
    echo "Migrating and collectstatic"
    python /home/ubuntu/obdev2018/manage.py migrate
    python /home/ubuntu/obdev2018/manage.py collectstatic --noinput
fi
python /home/ubuntu/obdev2018/manage.py collectstatic --noinput --settings=config.settings.static
