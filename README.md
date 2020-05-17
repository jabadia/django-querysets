# How to see queries

https://davit.tech/django-queryset-examples


1. Using logging

django.db -> DEBUG


getLogger('django.db').setLevel(logging.DEBUG)


from django.test.utils import CaptureQueriesContext

