from django.db import models


def get_name(instance, request):
    return getattr(instance, 'name', None)


GLOBAL_TRACK_FIELDS = [
    ('name', models.TextField(), get_name),
]
