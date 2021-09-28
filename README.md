# Real Estate Scraper

Real Estate Scraper is a project developed to compare property prices amongst similar real estate options close to each other.


### How does it work?

It works by extracting property prices and details from a Spanish website. The flow is the following:
1) The user inputs an Excel file with a list of properties he/she wants to analyze
2) The site interprets the file and lauches a scraping job for each inputed property
3) For each property:
   - A circunference around the property is cropped and posts of properties with similar characteristics are extracted.
   - If enough posts match the characteristics of the property in the selected region, they are saved in the database, but if they are not enough another search is done on a larger search area
   - An  average of cheapest posts (in €/m²) is calculated to compare with original property


### Visual flow

First of all, each user has to login so he/she can view only his/her jobs

![alt text](https://github.com/agusbegue/realestate-scraper/blob/master/data/screenshots/login.png?raw=true)

Once logged in, the user can view the jobs started, and their status. The user can either download the data in an excel file, delete de job, or view the job details

![alt text](https://github.com/agusbegue/realestate-scraper/blob/master/data/screenshots/dashboard.png?raw=true)

If the user decides to view the details, a new screen shows up in which he/she can see each property and the average price found

![alt text](https://github.com/agusbegue/realestate-scraper/blob/master/data/screenshots/properties.png?raw=true)


### Tools

The app uses frameworks [Django](https://www.djangoproject.com/) (for the website) and [Scrapy](https://scrapy.org/) (for web scraping).

The app has error reporting via a [Telegram Bots](https://core.telegram.org/bots)


### Visual flow
Add screenshots of flow

## How to use?

Clone the repository
```bash
git clone https://github.com/agusbegue/realestate-scraper.git
```

Install requirements
```bash
cd realestate-scraper
pip install -r requirements.txt
```

Run the migrations for django
```bash
python manage.py makemigrations
python manage.py migrate
```

Create user
```bash
python manage.py createsuperuser
```

Start Django server
```bash
python manage.py runserver
```

On another terminal, run the Scrapy background process
```bash
cd scrapy_app && scrapyd
```


You will have your web running so you can access [localhost:8000](http://localhost:8000) and start using it!

There is an example input file for you to try it [here](https://github.com/agusbegue/realestate-scraper/blob/master/data/example_input.xlsx)