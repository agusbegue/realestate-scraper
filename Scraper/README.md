python -m venv venv

venv\Scripts\activate


python manage.py makemigrations

python manage.py migrate


django runserver 8080

cd Scrapy/scrapy_app && scrapyd
