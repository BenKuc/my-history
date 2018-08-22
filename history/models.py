from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# import all models into this as django will only recognize them in the
# specified models module.
from .diffs.models import *
from .events import *


# XXX: pk and (model, id, duplication) are kinda duplicated data, but since
#      django does not support composed pks, it is okay.
class ObjectHistory(models.Model):
    composed_pk = models.CharField(
        max_length=255, primary_key=True, unique=True,
    )
    id = models.CharField(max_length=255)
    model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    history_object = GenericForeignKey(
        ct_field='model', fk_field='id',
    )
    duplication = models.PositiveIntegerField()

    class Meta:
        unique_together = ('object_pk', 'content_type', 'history_id', )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        qs = ObjectHistory.objects.filter(id=self.id)
        self.duplication = qs.count()
        if self._state.adding:
            self.duplication += 1
        self.composed_pk = '{}-{}-{}'.format(
            self.model.__name__, self.id, self.duplication,
        )
        super().save(force_insert, force_update, using, update_fields)

    def all_events(self):
        return self.events.all()

    def updates(self):
        return self.events.filter(type='U')

    def creation(self):
        return self.events.filter(type='C').first()

    def deletion(self):
        return self.events.filter(type='D').first()

    def all_tracks(self):
        events = self.events.select_related('after')
        return events.values_list('after', flat=True)

    def latest_track(self):
        return self.events.select_related('after').last().after

    def initial_track(self):
        return self.events.select_related('after').first().after


class HistoryBaseModel(models.Model):
    model = models.ForeignKey(
        'contenttypes.ContentType', on_delete=models.DO_NOTHING,
    )

    # TODO K1
    @property
    def previous(self):
        e = self.previous_event
        return e.before if hasattr(e, 'before') else None

    @property
    def next(self):
        e = self.next_event
        return e.after if hasattr(e, 'after') else None


class SimpleObjectReference(models.Model):
    model = models.ForeignKey(
        'contenttypes.ContentType', on_delete=models.CASCADE,
    )
    pk_value = models.CharField(max_length=255)
    instance = GenericForeignKey(fk_field='pk_value', ct_field='model')
