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
    # TODO: also history_id
    object_pk = models.PositiveIntegerField()


# TODO: make this dynamically by copying the pk field!
class SimpleObjectReferenceByString(SimpleObjectReference):
    # TODO: also history_id
    object_pk = models.CharField(max_length=255)


# TODO: maybe make this a history-descriptor, but move attributes to a
#       BaseClass for event
# TODO: also put special methods on this descriptor (like updates, events...)
# this is where all the history of an object is gathered together
class ObjectHistory(models.Model):
    # TODO: set this field dynamically -> how to handle different pk-fields
    #       -> assume that int and str will be enough actually
    object_pk = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    # TODO: overwrite AutoField and set as pk
    history_id = None  # TODO: this should be a field like: if the
                       # object_pk was duplicated in the original table
                       # this is the number of duplication in order!

    class Meta:
        unique_together = ('object_pk', 'content_type', 'history_id', )

    # TODO: this is for convenience: obj.history.<manager_method>
    def __getattribute__(self, item):
        try:
            # TODO: self.manager
            return getattr(self, item)
        except AttributeError:
            return super().__getattribute__(item)


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
