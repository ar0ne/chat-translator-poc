import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.safestring import mark_safe
from config.settings import SUPPORTED_LANGUAGES

SUPPORTED_LANG_CODES = [language[0] for language in SUPPORTED_LANGUAGES]


def index(request):
    return render(request, 'chat/index.html', {
        'roomNames': SUPPORTED_LANGUAGES
    })


def room(request, room_name):
    if room_name in SUPPORTED_LANG_CODES:
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(
                json.dumps(room_name)
            ),
        })
    return HttpResponseNotFound("Language is not supported!")
