from .models import *


def get_free_rooms():
    rooms = Room.objects.all()
    return rooms