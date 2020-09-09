# Web application for web scraping
Using Django + Scrapy

### Create environment
python -m venv venv  

venv\Scripts\activate

### Database migrations
python manage.py makemigrations

python manage.py migrate

### Deployment
#### - Option 1 (regular)
django runserver 8080

cd scrapy_app && scrapyd


#### - Option 2 (heroku)
heroku login

heroku create

git push heroku master
