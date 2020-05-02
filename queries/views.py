from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User


def first(request):
    # https://davit.tech/django-queryset-examples/#section-query
    users = User.objects.all()
    return JsonResponse({
        'users': list(users.values()),
        'query': str(users.query),
    })


def and_operation(request):
    # https://davit.tech/django-queryset-examples/#section-and
    qs1 = User.objects.filter(first_name='John', is_active=True)
    qs2 = User.objects.filter(first_name='John').filter(is_active=True)
    qs3 = User.objects.filter(first_name="John") & User.objects.filter(is_active=True)
    qs4 = User.objects.filter(Q(first_name="John") & Q(is_active=True))

    return JsonResponse({
        name: {
            'data': list(qs.values()),
            'query': str(qs.query),
        } for name, qs in [
            ('qs1', qs1),
            ('qs2', qs2),
            ('qs3', qs3),
            ('qs4', qs4),
        ]
    })

