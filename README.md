# ewallet

## Installation instructions
1. Make sure you have python > 3.7 Installed on your machine. [Download Python](https://www.python.org/downloads/).
2. Clone this repo using command on your terminal `git clone https://github.com/adityamuhammad/ewallet.git`
3. Run command on your terminal `pip install pipenv` if you dont install pipenv yet
4. Copy `.env.example` to `.env`, and fill the value of the variable, (fill JWT_SECRET_KEY and DATABASE_URI_DEV value. example: I use mysql database for this project, so fill the DATABASE_URI_DEV value with `mysql+pymysql://<username>:<password>@localhost/ewallet_dev`. Also dont forget to create database with the name ewallet_dev.
5. Run migration for database use command `make migrate_dev`, after that run command `make seed_dev` for creating seed data. 
6. Run command `pipenv shell` to activate the virtual environment          
7. Set variable FLASK_ENV to development. Run command on terminal `export FLASK_ENV=development`, if you are using Windows use command `set FLASK_ENV=development`
8. Set variable CONFIG_SETTING to config.Devconfig . Run command on terminal `export CONFIG_SETTING=config.DevConfig`, if you are using Windows use command `set CONFIG_SETTING=config.DevConfig`
9. To run application, use command `flask run`.

## Endpoints
Attempt | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 | #9 | #10 | #11
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |---
Seconds | 301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269
