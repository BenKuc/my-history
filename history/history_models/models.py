from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


class SimpleObjectReference(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # TODO: object_pk
    object_id = models.PositiveIntegerField()
    # TODO: is that really what we want or just the two above?
    referenced_object = GenericForeignKey('content_type', 'object_id')
