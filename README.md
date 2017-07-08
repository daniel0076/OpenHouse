
## Running on your host

### Dependency

#### pip

+ Django >= 1.9
+ django-ckeditor
+ Pillow
+ mysqlclient
+ Xlsxwriter

#### other
+ CKEditor

### Settings.py

Make sure your database username and password settings are correct

### Database Migration

+ `python manage.py makemigrations`
+ `python manage.py migrate`
+ `python manage.py migrate --database=2017`

### Run the development server

`python manage.py runserver [IP] [PORT]

