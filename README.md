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

## Endpoint
### 1. Login
Used for authenticating registered user, get access token stored in cookie with httponly set to true.

**URL** : `/token/auth`

**Method** : `POST`

**Auth required** : NO

**Request Body**

```json
{
    "email": "[valid email address]",
    "password": "[password in plain text]"
}
```

**Request Header**
use default request header

#### Success Response
set access_token_cookie,csrf_access_token,refresh_token_cookie,csrf_refresh_token in header response

**Code** : `200 OK`

**Response body**

```json
{
    "msg": "login success."
}
```

#### Error Response

**Condition** : If 'email' and 'password' combination is wrong.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "msg": "login failed."
}
```

### 2. Refresh token
Used for refresh access token

**URL** : `/token/refresh`

**Method** : `POST`

**Auth required** : NO

**Request Body**
None

**Request Header**
```json
{
    "X-CSRF-TOKEN": "[csrf_refresh_token]",
    "refresh_token_cookie": "[refresh_token_cookie]"
}
```

#### Success Response

**Code** : `200 OK`

**Response body**

```json
{
    "msg": "token refreshed."
}
```

#### Error Response

**Condition** : If request header invalid.

**Code** : `401 UNAUTHORIZED`

**Content** :

```json
{
    "msg": "whether csrf token refresh or refresh token invalid"
}
```

### 3. remove token or logout
Used for remove access token

**URL** : `/token/remove`

**Method** : `POST`

**Auth required** : NO

**Request Body**
None

**Request Header**
None
### Success Response

**Code** : `200 OK`

**Response body**

```json
{
    "msg": "logout success."
}
```

### 4. Topup
Used for topup

**URL** : `/api/topup`

**Method** : `POST`

**Auth required** : YES

**Request Body**
```json
{
    "amount": "[amount]",
}
```


**Request Header**
```json
{
    "X-CSRF-TOKEN": "[csrf_access_token]",
    "location": "[client location]",
    "ip-address": "[ip-address client]"
}
```

### Success Response

**Code** : `200 OK`

**Response body**

```json
{
    "msg": "transaction success."
}
```

### Error Response

**Condition** : If request send is invalid.
**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "msg": "transaction failed."
}
```

### 4. Transfer
Used for transfer

**URL** : `/api/transfer`

**Method** : `POST`

**Auth required** : YES

**Request Body**
```json
{
    "amount": "[amount]",
    "code": "[code]"
}
```


**Request Header**
```json
{
    "X-CSRF-TOKEN": "[csrf_access_token]",
    "location": "[client location]",
    "ip-address": "[ip-address client]"
}
```

### Success Response

**Code** : `200 OK`

**Response body**

```json
{
    "msg": "transaction success."
}
```

### Error Response

**Condition** : If request send is invalid.
**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "msg": "transaction failed."
}
```
