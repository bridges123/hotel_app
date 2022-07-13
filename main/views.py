from django.shortcuts import render
from django.http import HttpRequest, JsonResponse


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        'status': 200,
        'error': False,
        'message': 'Some message'
    })
