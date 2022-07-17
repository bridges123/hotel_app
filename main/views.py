from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from . import utils


def index(request: HttpRequest):
    context = {
        'rooms': utils.get_free_rooms()
    }
    return render(request, 'main/index.html', context=context)
