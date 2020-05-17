![](https://github.com/jabadia/django-querysets/workflows/.github/workflows/main.yml/badge.svg)

# Purpose
This repo is a sample for:
a) writing different types of SQL queries using Django ORM, following the examples in https://davit.tech/django-queryset-examples
b) running unit-tests in GitHub Actions including PostgreSQL

# Random n1otes
## How to see queries

```
Using logging
django.db -> DEBUG
getLogger('django.db').setLevel(logging.DEBUG)
from django.test.utils import CaptureQueriesContext

        - "postgres"
#        - "-c"
#        - "log_statement=all"
```
