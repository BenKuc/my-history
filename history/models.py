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
    history_id = None

    class Meta:
        # TODO: could be that original pk is re-given to a model -> problem
        unique_together = ('object_pk', 'content_type', )


class ManagerEvent(models.Model):
    pass


class ObjectEvent(models.Model):
    super_event = models.OneToOneField(ManagerEvent)
    # TODO: related_query_name?
    object_history = models.ForeignKey(ObjectHistory, related_name='events')
    history_date = ''
    type = ['UPDATE', 'CREATE', 'BULK_CREATE', 'BULK_UPDATE', ]
    # TODO: maybe wrap all create/update methods on queryset
    #       to get accurate all types
    trigger = ['save', 'bulk_create', 'bulk_update']  # TODO: move to ManagerEvent

    def __str__(self):
        return '{type}-event triggered by '

    # TODO: order_by history_date!


# TODO: check constraints for before and after
# TODO: maybe remove this in favor of ObjectEvent -> type is a computed value by before and after -> get control over setattr by type
# TODO: do check constraints that prevent saving before/after when the type is create/update -> sql
class Creation(Event):
    after = models.ForeignKey('history.PseudoHistoryModel', related_name='previous_event')


class Update(Event):
    before = models.ForeignKey('history.PseudoHistoryModel', related_name='next_Event')
    after = models.ForeignKey('history.PseudoHistoryModel', related_name='previous_event')


class Deletion(Event):
    before = models.ForeignKey('history.Pseudo...', related_name='next_event')


# TODO: write base_class for this
# TODO: o2o to this model by event
# TODO: o2o-extension by multi-table-inheritance from this model to the actual
#       history_model -> this is a base-class: HistoryModel
class PseudoHistoryModel(models.Model):

    @property
    def previous(self):
        e = self.previous_event
        return e.before if hasattr(e, 'before') else None

    @property
    def next(self):
        e = self.next_event
        return e.after if hasattr(e, 'after') else None
