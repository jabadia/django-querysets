import logging
from datetime import timedelta

import django.urls as urls
from django.db import connection
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

logger = logging.getLogger(__name__)


def index(request):
    resolver = urls.get_resolver()
    all_urls = ['/' + v[0][0][0] for v in resolver.reverse_dict.values()]
    all_urls.reverse()
    return render(request, 'queries/index.html', {'urls': all_urls})


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


def or_operation(request):
    # https://davit.tech/django-queryset-examples/#section-or
    qs1 = User.objects.filter(Q(first_name="John") | Q(first_name="Jane"))
    qs2 = User.objects.filter(first_name="John") | User.objects.filter(first_name="Jane")

    return JsonResponse({
        name: {
            'data': list(qs.values()),
            'query': str(qs.query),
        } for name, qs in [
            ('qs1', qs1),
            ('qs2', qs2),
        ]
    })


def not_equal(request):
    # https://davit.tech/django-queryset-examples/#section-not-equal
    qs1 = User.objects.filter(~Q(first_name="John"))
    qs2 = User.objects.exclude(first_name="John")

    return JsonResponse({
        name: {
            'data': list(qs.values()),
            'query': str(qs.query),
        } for name, qs in [
            ('qs1', qs1),
            ('qs2', qs2),
        ]
    })


def in_filtering(request):
    # https://davit.tech/django-queryset-examples/#section-in
    qs = User.objects.filter(pk__in=[1, 4, 7])
    with CaptureQueriesContext(connection) as ctx:
        bulk = User.objects.in_bulk([1, 4, 7])
        for k, v in bulk.items():
            bulk[k] = model_to_dict(v, exclude=['groups', 'user_permissions'])
    assert len(ctx.captured_queries) == 1, "bad number of queries executed"
    return JsonResponse({
        'qs': {
            'data': list(qs.values()),
            'query': str(qs.query),
        },
        'bulk': {
            'data': bulk,
            'query': ctx.captured_queries[0]['sql'],
        }
    })


def is_null(request):
    # https://davit.tech/django-queryset-examples/#section-isnull
    is_null_qs = User.objects.filter(first_name__isnull=True)
    is_not_null_qs = User.objects.filter(first_name__isnull=False)
    return JsonResponse({
        name: {
            'data': list(qs.values()),
            'query': str(qs.query),
        } for name, qs in [
            ('is_null_qs', is_null_qs),
            ('is_not_null_qs', is_not_null_qs),
        ]
    })


def like(request):
    # https://davit.tech/django-queryset-examples/#section-like
    startswith_qs = User.objects.filter(first_name__startswith="Jo")
    endswith_qs = User.objects.filter(first_name__endswith="yan")
    contains_qs = User.objects.filter(first_name__contains="oh")
    regex_qs = User.objects.filter(last_name__regex=r"^D.e$")

    return JsonResponse({
        name: {
            'data': list(qs.values()),
            'query': str(qs.query),
        } for name, qs in [
            ('startswith_qs', startswith_qs),
            ('endswith_qs', endswith_qs),
            ('contains_qs', contains_qs),
            ('regex_qs', regex_qs),
        ]
    })


def comparison(request):
    # https://davit.tech/django-queryset-examples/#section-comparsion
    gt_qs = User.objects.filter(id__gt=2)
    lt_qs = User.objects.filter(id__lt=2)
    gte_qs = User.objects.filter(id__gte=2)
    lte_qs = User.objects.filter(id__lte=2)

    return JsonResponse({
        name: {
            'data': list(qs.values()),
            'query': str(qs.query),
        } for name, qs in [
            ('gt_qs', gt_qs),
            ('lt_qs', lt_qs),
            ('gte_qs', gte_qs),
            ('lte_qs', lte_qs),
        ]
    })


def between(request):
    # https://davit.tech/django-queryset-examples/#section-between
    today = timezone.now()
    two_weeks_ago = today - timedelta(days=14)
    between_qs = User.objects.filter(date_joined__range=[two_weeks_ago, today])

    return JsonResponse({
        name: {
            'data': list(qs.values()),
            'query': str(qs.query),
        } for name, qs in [
            ('between_qs', between_qs),
        ]
    })


def limit(request):
    # https://davit.tech/django-queryset-examples/#section-limit
    limit_qs = User.objects.all()[:10]
    offset_limit_qs = User.objects.all()[10:20]

    return JsonResponse({
        name: {
            'data': list(qs.values()),
            'query': str(qs.query),
        } for name, qs in [
            ('limit_qs', limit_qs),
            ('offset_limit_qs', offset_limit_qs),
        ]
    })


def orderby(request):
    by_date_joined_qs = User.objects.order_by('date_joined')
    by_multiple_qs = User.objects.order_by('date_joined', '-last_name')
    by_reverse_date_joined_qs = User.objects.order_by('date_joined').reverse()
    by_random_qs = User.objects.order_by('?')

    return JsonResponse({
        name: {
            'data': list(qs.values()),
            'query': str(qs.query),
        } for name, qs in [
            ('by_date_joined_qs', by_date_joined_qs),
            ('by_multiple_qs', by_multiple_qs),
            ('by_reverse_date_joined_qs', by_reverse_date_joined_qs),
            ('by_random_qs', by_random_qs),
        ]
    })


def get_single(request):
    with CaptureQueriesContext(connection) as ctx:
        user_using_limit = User.objects.all()[0]
        user_using_get = User.objects.get(pk=1)
        user_using_first = User.objects.order_by('date_joined', '-first_name').first()
        user_using_last = User.objects.order_by('first_name').last()
        user_using_earliest = User.objects.earliest('date_joined', '-first_name')
        user_using_latest = User.objects.latest('first_name')

    assert 6 == len(ctx.captured_queries), "bad number of queries executed"

    return JsonResponse({
        name: {
            'data': model_to_dict(user_instance, exclude=['groups', 'user_permissions']),
            'query': query['sql'],
        } for (name, user_instance), query in zip([
            ('user_using_limit', user_using_limit),
            ('user_using_get', user_using_get),
            ('user_using_first', user_using_first),
            ('user_using_last', user_using_last),
            ('user_using_earliest', user_using_earliest),
            ('user_using_latest', user_using_latest),
        ], ctx.captured_queries)
    })


def joins(request):
    users_with_group_name_qs = User.objects.all().values('username', 'first_name', 'last_name', 'groups__name')
    groups_with_users_qs = Group.objects.all().values('name', 'user__username')

    return JsonResponse({
        name: {
            'data': list(qs),
            'query': str(qs.query),
        } for name, qs in [
            ('users_with_group_name_qs', users_with_group_name_qs),
            ('groups_with_users_qs', groups_with_users_qs),
        ]
    })
