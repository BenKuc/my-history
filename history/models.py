from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
# TODO: import all models here
from .diffs.models import *
from .events import *


# TODO: do we really want this?
class TrackTracker(models.Model):
    model = models.ForeignKey('contenttypes.ContentType')
    history_model = models.ForeignKey('contenttypes.ConentType')
    # TODO: maybe table-name and so one -> corresponding to settings


class SimpleObjectReference(models.Model):
    model = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)

    # TODO: make this a manager
    @property
    def get_object(self):
        try:
            return self.model.objects.get(pk=self.object_pk)
        except models.ObjectDoesNotExist:
            return None

    class Meta:
        abstract = True


# TODO: make this dynamically by copying the pk field!
class SimpleObjectReferenceById(SimpleObjectReference):
    object_pk = models.PositiveIntegerField()


# TODO: make this dynamically by copying the pk field!
class SimpleObjectReferenceByString(SimpleObjectReference):
    object_pk = models.CharField(max_length=255)


# this is where all the history of on object is gathered together
class ObjectHistory(models.Model):
    # TODO: set this field dynamically
    object_pk = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)

    class Meta:
        # TODO: could be that original pk is re-given to a model -> problem
        unique_together = ('object_pk', 'content_type', )


class Event(models.Model):
    # TODO: related_query_name?
    central = models.ForeignKey(ObjectHistory, related_name='events')
    history_date = ''
    type = ['UPDATE', 'CREATE', 'BULK_CREATE', 'BULK_UPDATE', ]

    # TODO: check constraints for before and after


class Creation(Event):
    after = models.ForeignKey('history.PseudoHistoryModel', related_name='previous_event')


class Update(Event):
    before = models.ForeignKey('history.PseudoHistoryModel', related_name='next_Event')
    after = models.ForeignKey('history.PseudoHistoryModel', related_name='previous_event')


class Deletion(Event):
    before = models.ForeignKey('history.Pseudo...', related_name='next_event')


# TODO: write base_class for this
class PseudoHistoryModel(models.Model):

    @property
    def previous(self):
        e = self.previous_event
        return e.before if hasattr(e, 'before') else None

    @property
    def next(self):
        e = self.next_event
        return e.after if hasattr(e, 'after') else None
