from django.http import JsonResponse
from django.contrib.auth.models import User


def first(request):
    users = User.objects.all()
    return JsonResponse({
        'users': list(users.values()),
        'query': str(users.query),
    })
