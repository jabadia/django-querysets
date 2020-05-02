from django.http import JsonResponse
from django.contrib.auth.models import User


def first(request):
    # https://davit.tech/django-queryset-examples/#section-query
    users = User.objects.all()
    return JsonResponse({
        'users': list(users.values()),
        'query': str(users.query),
    })
