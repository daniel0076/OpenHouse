
## Running on your host

### Dependency

+ CKEditor
+ django-ckeditor

### Settings.py

Make sure your database username and password settings are correct

### Database Migration

+ `python manage.py makemigrations`
+ `python manage.py migrate`
+ `python manage.py migrate --database=2016`

### Run the development server

`python manage.py runserver [IP] [PORT]

