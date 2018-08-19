from django.contrib.contenttypes.models import ContentType
from django.db import models


class SimpleObjectReference(models.Model):
    model = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    @property
    def get_object(self):
        try:
            return self.model.objects.get(pk=self.object_pk)
        except models.ObjectDoesNotExist:
            return None

    class Meta:
        abstract = True


class SimpleObjectReferenceById(SimpleObjectReference):
    object_pk = models.PositiveIntegerField()


class SimpleObjectReferenceByString(SimpleObjectReference):
    object_pk = models.CharField(max_length=255)
