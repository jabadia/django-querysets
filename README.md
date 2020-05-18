![](https://github.com/jabadia/django-querysets/workflows/run%20unit%20tests/badge.svg)

# Purpose
This repo is a sample for:

a) writing different types of SQL queries using Django ORM, following the examples in https://davit.tech/django-queryset-examples

b) running unit-tests in GitHub Actions including PostgreSQL

# Random notes
## How to see queries
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



```
Using logging
django.db -> DEBUG
getLogger('django.db').setLevel(logging.DEBUG)
from django.test.utils import CaptureQueriesContext

        - "postgres"
#        - "-c"
#        - "log_statement=all"
```
