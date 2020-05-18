![](https://github.com/jabadia/django-querysets/workflows/run%20unit%20tests/badge.svg)

# Purpose
This repo is a sample for:

a) writing different types of SQL queries using Django ORM, following the examples in https://davit.tech/django-queryset-examples

b) running unit-tests in GitHub Actions including PostgreSQL

# How to use

## 1. Download the repo:
```
git clone git@github.com:jabadia/django-querysets.git
```

## 2. Install dependencies:
```
cd django-querysets
pipenv sync
```

## 3. Decide if you want to run tests against a local postgres server or launch a docker container postgres server

### 3.1 Running tests on your local postgres server

Export variables pointing to your local server (tests will run in a newly created database named `test_queries`)
```
export POSTGRES_PORT=5432
export POSTGRES_USER=<user>
export POSTGRES_PASSWORD=<pass>
```

### 3.2 Running tests on a postgres server inside a docker container

```
# in another terminal
cd db
docker-compose up
```

```
export POSTGRES_PORT=5556
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=secretpass
```
 
## 4. Run tests
```
DJANGO_SETTINGS_MODULE=querysets.test_settings pipenv run python manage.py test

# or

export DJANGO_SETTINGS_MODULE=querysets.test_settings
pipenv run python manage.py test
```

## 5. Run server
```
# create the production database
PGPASSWORD=secretpass createdb -h localhost -p 5556 queries -U postgres --no-password

# launch the server
export DJANGO_SETTINGS_MODULE=querysets.test_settings  
pipenv run python manage.py migrate
pipenv run python manage.py runserver 7777

```
open your browser pointing to [http://localhost/7777](http://localhost/7777)


# How to see queries

## 1. LOGGING options in settings
In `settings.py` look for the `LOGGING` key and enable `django.db` DEBUG level
```
LOGGING = {
    ...
    'loggers': {
        ...
        'django.db': {
            'level': 'DEBUG',  # log SQL queries
        },
    },
}
```

## 2. Using logging selectively: getLogger('django.db').setLevel()
In any place of the code where you want to log queries, enable it by writing:

```
getLogger('django.db').setLevel(logging.DEBUG)
```

## 3. CaptureQueriesContext
Using a query capture context manager in one particular place of the code:

```
from django.test.utils import CaptureQueriesContext
from django.db import connection
...

def one_function():
    ...
    with CaptureQueriesContext(connection( as queries:
        < call function or execute code that launches queries here >
        ...

    for query in queries.captured_queries:
        print(query)
```

## 4. Enabling server-side logging in postgres (easier in a docker container hosted postgres)

In `docker-compose.yml` uncomment the logging option:
```
        - "postgres"
#        - "-c"                     # uncomment this
#        - "log_statement=all"      # uncomment this
```
