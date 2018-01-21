# avt_checktwfriends Django RESTful API project


## 1. Introduction

Active Twitter users who have many friends(following) often find it difficult to identify those who are no longer their followers. However, users who are no longer followers continue to be friends(following).

Maintain the actual state of the list of your friends on Twitter with the `avt_checktwfriends` project simply:
1. Check your friends(following) on Twitter who are not followers
2. Mark those friends(following) with whom you wish to keep friendship
3. Destroy friendship(unfollow) with all the other friends(following)

`avt_checktwfriends` is a CRUD-based RESTful API project with Django and Django REST Framework.



## 2. Requirements

### 2.1 `avt_checktwfriends` project requires the following **main components**:

* [Python 3.6.3](https://www.python.org/) - Python is a programming language that lets you work quickly
* [Django 1.11.8](https://www.djangoproject.com/) - A high-level Python Web framework
* [Django REST Framework 3.7.7](http://www.django-rest-framework.org/) - A powerful and flexible toolkit for building Web APIs
* [python-twitter 3.3](https://github.com/bear/python-twitter) - A Python wrapper around the Twitter API
* [Postgres 10.1](https://www.postgresql.org/) - PostgreSQL is a powerful, open source object-relational database system
* [Psycopg2 2.7.3.2](http://initd.org/psycopg/)  - Psycopg is the most popular PostgreSQL adapter for the Python programming language.

### 2.2 The following packages **are optional**, but very useful:

* [coreapi 2.3.3](http://www.coreapi.org/) - Schema generation support
* [coreapi-cli 1.0.6](http://www.coreapi.org/) - Command-line tool that you can use to interact with APIs
* [Markdown 2.6.9](https://python-markdown.github.io/) - Markdown support for the browsable API
* [httpie 0.9.9](https://github.com/jakubroztocil/httpie) - Modern command line HTTP client

## 3. How to prepare and start using this project step by step

### 3.1 Fork, Clone or Download the project

### 3.2 Install the requirements

### 3.3 Create a Postgres database called `avt_checktwfriends`

### 3.4 Instead of data placeholders, add your real data to the following project files:

#### 3.4.1 To interact with Postgres database

```python
# avt_checktwfrinds/avt_checktwfrinds/settings.py

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'avt_checktwfriends',
        'USER': '<your-user>', # by default 'postgres'
        'PASSWORD': '<your-password>',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

#### 3.4.2 To interact with your Twitter account need create Twitter App, and getting your application tokens

> In order to use the python-twitter API client, you first need to acquire a set of application tokens.
> - [python-twitter documentation](https://python-twitter.readthedocs.io/en/latest/getting_started.html)

```python
# avt_checktwfrinds/avt_checktwfrinds/settings.py

# Authentication data for Twitter App created for Twitter Account
# https://apps.twitter.com/
CONSUMER_KEY = '<your-CONSUMER_KEY>' 
CONSUMER_SECRET = '<your-CONSUMER_SECRET>' 
ACCESS_TOKEN = '<your-ACCESS_TOKEN>' 
ACCESS_TOKEN_SECRET = '<your-ACCESS_TOKEN_SECRET>'
```

#### 3.4.3 To successfully run unit tests for views:

You need specify the screen names of REAL Twitter users as follow:
```python
# avt_checktwfrinds/api/tests/test_views.py

class NotFollowersTwFriendsNeedUnfollowUpdateTestCase(APITestCase):
    """
    Test the API which update need_unfollow status for not_follower_tw_friend
    from 'not_unfollow_tw_friends_screen_name_list' with 'need_unfollow=False'
    (all the existing Twitter friends who aren't followers and not selected for unfollow)
    """

    # A test list that contains 'screen_names' of all the existing Twitter friends
    # who aren't followers and not selected for unfollow.
    # NOTE: To successfully run the test, you need specify
    # the screen names of REAL Twitter users.
    not_unfollow_tw_friends_screen_name_list = [
        '<real_tw_user_screen_name_1 from your account>',
        '<real_tw_user_screen_name_2 from your account>',
        '<real_tw_user_screen_name_3 from your account>',
        '<...>',
        '<real_tw_user_screen_name_N from your account>'
    ]
```

Run the unit test with the following console command:

`$ python manage.py test api.tests.test_views`


### 3.5 Apply the migrations

`$ python manage.py makemigrations api`

> By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.
> - [Django 1.11 documentation](https://docs.djangoproject.com/en/1.11/intro/tutorial02/)


`$ python manage.py migrate`

> Run migrate to apply changes from models to the database.
> - [Django 1.11 documentation](https://docs.djangoproject.com/en/1.11/intro/tutorial02/)

### 3.6 Create a superuser who will have permissions to the our API endpoints

`$ python manage.py createsuperuser`

### 3.7 Start the development server

`$ python manage.py runserver`


## 4. Examples of using our API

Ways to access the API of our project:
* Directly through the browser (The Web browsable API from Django REST Framework)
* Using command-line tools like HTTPie, cURL, coreapi-cli, etc.
* Using the Complete API Development Environment like Postman

### 4.1 Obtain authentication Token using HTTPie, command-line tool

API endpoint URL:

`http://localhost:8000/api/v1/token/`

HTTPie CLI command:

`$ http --json POST http://localhost:8000/api/v1/token/ username=<your-superuser-username> password=<your-superuser-password>`

Response result in JSON:
```json
HTTP/1.0 200 OK
...

{
    "token": "<your-generated-token>"
}
```

### 4.2 Return the explicitly defined schema view for automatically generated schema 

### 4.2.1 Using HTTPie, command-line tool

API endpoint URL:

`http://localhost:8000/api/v1/schema/`


HTTPie CLI command:

`$ http --json -a <your-superuser-username>:<your-superuser-password> GET http://localhost:8000/api/v1/schema/`

Response result in JSON:

```json
HTTP/1.0 200 OK
...
{
    "_type": "document",
    "_meta": {
        "url": "http://localhost:8000/api/v1/schema/",
        "title": "avt_checktwfriends API schema"
    },
    "not_followers_tw_friends": {
        "check": {
            "list": {
                "_type": "link",
                "url": "/api/v1/not_followers_tw_friends/check/",
                "action": "get",
                "description": "Return an updated list(after check) of all the existing Twitter friends\nwho aren't followers."
            }
        },
"_comment": "..."
```

### 4.2.2 Using The Web browsable API from Django REST Framework

API endpoint URL:

`http://localhost:8000/api/v1/schema/`

STEP 1. Authentication required for API endpoint
![avt_checktwfriends project. Authentication required for API endpoint.](https://software.avt.dn.ua/wp-content/uploads/2018/01/avtsoft_avt_checktwfriends_api_v1_schema_1_800x614.png)

STEP 2. Return the explicitly defined schema view for automatically generated schema
![avt_checktwfriends project. Return the explicitly defined schema view for automatically generated schema.](https://software.avt.dn.ua/wp-content/uploads/2018/01/avtsoft_avt_checktwfriends_api_v1_schema_2_800x616.png)


### 4.3 Return the documentation page with automatically generated schema

API endpoint URL:

`http://localhost:8000/api/v1/docs/`

Display in the browser window avt_checktwfriends API docs

![Display in the browser window avt_checktwfriends API docs](https://software.avt.dn.ua/wp-content/uploads/2018/01/avtsoft_avt_checktwfriends_api_v1_docs_800x616.png)



### 4.4 Return a list of all the existing Twitter friends(following) who aren't followers

API endpoint URL:

`http://localhost:8000/api/v1/not_followers_tw_friends/`


HTTPie CLI command:

`$ http --json -a <your-superuser-username>:<your-superuser-password> GET http://localhost:8000/api/v1/not_followers_tw_friends/`


Response result in JSON:
(**NOTE:** The data of Twitter users are fictitious and not related to real accounts)

```json
HTTP 200 OK
...

[
    {
        "id_str": "123456789",
        "screen_name": "tw_user_1",
        "name": "Twitter User #1",
        "description": "Twitter User #1 description",
        "statuses_count": 120,
        "followers_count": 2821,
        "friends_count": 915,
        "created_at": "Mon Jan 01 00:00:00 +0000 2018",
        "location": "Helsinki, Finland",
        "avg_tweetsperday": "6.00",
        "tff_ratio": "3.08",
        "need_unfollow": false
    },
    {
        "id_str": "213456789",
        "screen_name": "tw_user_2",
        "name": "Twitter User #2",
        "description": "Twitter User #2 description",
        "statuses_count": 80,
        "followers_count": 720,
        "friends_count": 277,
        "created_at": "Tue Jan 02 15:05:10 +0000 2018",
        "location": "Stockholm, Sweden",
        "avg_tweetsperday": "4.20",
        "tff_ratio": "2.59",
        "need_unfollow": false
    },
    {
        "id_str": "312456789",
        "screen_name": "tw_user_3",
        "name": "Twitter User #3",
        "description": "Twitter User #3 description",
        "statuses_count": 45,
        "followers_count": 2521,
        "friends_count": 265,
        "created_at": "Tue Jan 03 10:27:03 +0000 2018",
        "location": "",
        "avg_tweetsperday": "2.65",
        "tff_ratio": "9.51",
        "need_unfollow": true
    }
]
```

### 4.5 Return an updated list(after check) of all the existing Twitter friends(following) who aren't followers

API endpoint URL:

`http://localhost:8000/api/v1/not_followers_tw_friends/check/`


HTTPie CLI command:

`$ http --json -a <your-superuser-username>:<your-superuser-password> GET http://localhost:8000/api/v1/not_followers_tw_friends/check/`


Response result in JSON:
(**NOTE:** The data of Twitter users are fictitious and not related to real accounts)

```json
HTTP 200 OK
...

[
    {
        "id_str": "123456789",
        "screen_name": "tw_user_1",
        "name": "Twitter User #1",
        "description": "Twitter User #1 description",
        "statuses_count": 120,
        "followers_count": 2821,
        "friends_count": 915,
        "created_at": "Mon Jan 01 00:00:00 +0000 2018",
        "location": "Helsinki, Finland",
        "avg_tweetsperday": "6.00",
        "tff_ratio": "3.08",
        "need_unfollow": false
    },
    {
        "id_str": "213456789",
        "screen_name": "tw_user_2",
        "name": "Twitter User #2",
        "description": "Twitter User #2 description",
        "statuses_count": 80,
        "followers_count": 720,
        "friends_count": 277,
        "created_at": "Tue Jan 02 15:05:10 +0000 2018",
        "location": "Stockholm, Sweden",
        "avg_tweetsperday": "4.20",
        "tff_ratio": "2.59",
        "need_unfollow": false
    },
    {
        "id_str": "312456789",
        "screen_name": "tw_user_3",
        "name": "Twitter User #3",
        "description": "Twitter User #3 description",
        "statuses_count": 45,
        "followers_count": 2521,
        "friends_count": 265,
        "created_at": "Tue Jan 03 10:27:03 +0000 2018",
        "location": "",
        "avg_tweetsperday": "2.65",
        "tff_ratio": "9.51",
        "need_unfollow": true
    },
    {
        "id_str": "412356789",
        "screen_name": "tw_user_4",
        "name": "Twitter User #4",
        "description": "Twitter User #3 description",
        "statuses_count": 721,
        "followers_count": 125,
        "friends_count": 431,
        "created_at": "Tue Dec 05 16:27:03 +0000 2017",
        "location": "London, UK",
        "avg_tweetsperday": "1.84",
        "tff_ratio": "0.29",
        "need_unfollow": true
    }    
]
```

### 4.6 Return a list of all the existing Twitter friends(following) who aren't followers and selected for unfollow ('need_unfollow' field value is True)

API endpoint URL:

`http://localhost:8000/api/v1/not_followers_tw_friends/need_unfollow/`


HTTPie CLI command:

`$ http --json -a <your-superuser-username>:<your-superuser-password> GET http://localhost:8000/api/v1/not_followers_tw_friends/need_unfollow/`


Response result in JSON:
(**NOTE:** The data of Twitter users are fictitious and not related to real accounts)

```json
HTTP 200 OK
...

[
    {
        "id_str": "312456789",
        "screen_name": "tw_user_3",
        "name": "Twitter User #3",
        "description": "Twitter User #3 description",
        "statuses_count": 45,
        "followers_count": 2521,
        "friends_count": 265,
        "created_at": "Tue Jan 03 10:27:03 +0000 2018",
        "location": "",
        "avg_tweetsperday": "2.65",
        "tff_ratio": "9.51",
        "need_unfollow": true
    },
    {
        "id_str": "412356789",
        "screen_name": "tw_user_4",
        "name": "Twitter User #4",
        "description": "Twitter User #3 description",
        "statuses_count": 721,
        "followers_count": 125,
        "friends_count": 431,
        "created_at": "Tue Dec 05 16:27:03 +0000 2017",
        "location": "London, UK",
        "avg_tweetsperday": "1.84",
        "tff_ratio": "0.29",
        "need_unfollow": true
    }
]
```

### 4.7 Update `need_unfollow` status for `not_follower_tw_friend` with `screen_name=tw_friend_screen_name`

API endpoint URL:

`http://localhost:8000/api/v1/not_followers_tw_friends/need_unfollow/update/tw_friend_screen_name/ need_unfollow=(True|False)`


HTTPie CLI command that sets `need_unfollow=False` for the specified Twitter `screen_name`:

`$ http --json -a <your-superuser-username>:<your-superuser-password> PATCH http://localhost:8000/api/v1/not_followers_tw_friends/need_unfollow/update/tw_user_4/ need_unfollow=False`


Response result in JSON:
(**NOTE:** The data of Twitter users are fictitious and not related to real accounts)

```json
HTTP 200 OK
...

[
    {
        "id_str": "412356789",
        "screen_name": "tw_user_4",
        "name": "Twitter User #4",
        "description": "Twitter User #3 description",
        "statuses_count": 721,
        "followers_count": 125,
        "friends_count": 431,
        "created_at": "Tue Dec 05 16:27:03 +0000 2017",
        "location": "London, UK",
        "avg_tweetsperday": "1.84",
        "tff_ratio": "0.29",
        "need_unfollow": false
    }    
]
```

HTTPie CLI command that sets `need_unfollow=True` for the specified Twitter `screen_name`:

`$ http --json -a <your-superuser-username>:<your-superuser-password> PATCH http://localhost:8000/api/v1/not_followers_tw_friends/need_unfollow/update/tw_user_4/ need_unfollow=True`


Response result in JSON:
(**NOTE:** The data of Twitter users are fictitious and not related to real accounts)

```json
HTTP 200 OK
...

[
    {
        "id_str": "412356789",
        "screen_name": "tw_user_4",
        "name": "Twitter User #4",
        "description": "Twitter User #3 description",
        "statuses_count": 721,
        "followers_count": 125,
        "friends_count": 431,
        "created_at": "Tue Dec 05 16:27:03 +0000 2017",
        "location": "London, UK",
        "avg_tweetsperday": "1.84",
        "tff_ratio": "0.29",
        "need_unfollow": true
    }   
]
```

### 4.8 Unfollow `not_followers_tw_friends` with `need_unfollow=True`, and return a list of all the existing Twitter friends(following) who aren't followers with `need_unfollow=False`

API endpoint URL:

`http://localhost:8000/api/v1/not_followers_tw_friends/unfollow/`


HTTPie CLI command:

`$ http --json -a <your-superuser-username>:<your-superuser-password> DELETE http://localhost:8000/api/v1/not_followers_tw_friends/unfollow/`


Response result in JSON:
(**NOTE:** The data of Twitter users are fictitious and not related to real accounts)

```json
HTTP 200 OK
...

[
    {
        "id_str": "123456789",
        "screen_name": "tw_user_1",
        "name": "Twitter User #1",
        "description": "Twitter User #1 description",
        "statuses_count": 120,
        "followers_count": 2821,
        "friends_count": 915,
        "created_at": "Mon Jan 01 00:00:00 +0000 2018",
        "location": "Helsinki, Finland",
        "avg_tweetsperday": "6.00",
        "tff_ratio": "3.08",
        "need_unfollow": false
    },
    {
        "id_str": "213456789",
        "screen_name": "tw_user_2",
        "name": "Twitter User #2",
        "description": "Twitter User #2 description",
        "statuses_count": 80,
        "followers_count": 720,
        "friends_count": 277,
        "created_at": "Tue Jan 02 15:05:10 +0000 2018",
        "location": "Stockholm, Sweden",
        "avg_tweetsperday": "4.20",
        "tff_ratio": "2.59",
        "need_unfollow": false
    }
]
```
