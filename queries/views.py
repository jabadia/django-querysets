from django.http import JsonResponse


def first(request):
    return JsonResponse({
        'data': {}
    })
