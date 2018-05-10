# info_security

1. Create and activate virtual env
`virtualenv -p /usr/local/bin/python3 env && source env/bin/activate`
2. install Requirements
`pip install -r requirements.txt`
3. Run Application:
`cd secretsapp && python manage.py runserver`



* let's add Faker and pillows as requirements, we might need them for easily createing entries and for saving images
* also: pip install bcrypt and pip install django[argon2]

* I think templates are supposed to be in top level directory, I moved index.html there

added superuser for db.  username: CSI. email: csi@unibz.it  password: superprotected  But  I don't know if it database and stuff
will come with push.

added populator.py - run to populate db if git doesn't transfer it.

to create db, run this commands:

* python manage.py migrate
* python manage.py makemigrations secretsmodules
* python manage.py migrate 
