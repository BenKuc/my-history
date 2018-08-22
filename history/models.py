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
    duplication = models.PositiveSmallIntegerField()

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

    # TODO: implementation of these methods are dependent on events! ->
    #       also look at HistoryBaseModel

    def all(self):
        pass

    def updates(self):
        return

    def events(self):
        pass

    def creation(self):
        pass

    def deletion(self):
        pass

    def manager_events(self):
        pass

    def history_events(self):
        pass


# TODO: o2o to this model by event
# TODO: o2o-extension by multi-table-inheritance from this model to the actual
#       history_model -> this is a base-class: HistoryModel
class HistoryBaseModel(models.Model):
    # TODO: you can do the django trick here with type:
    # (deletion, upadte, creation)

    @property
    def previous(self):
        e = self.previous_event
        return e.before if hasattr(e, 'before') else None

    @property
    def next(self):
        e = self.next_event
        return e.after if hasattr(e, 'after') else None


# TODO: do we really want this?
class TrackTracker(models.Model):
    model = models.ForeignKey('contenttypes.ContentType')
    history_model = models.ForeignKey('contenttypes.ConentType')
    # TODO: maybe table-name and so one -> corresponding to settings


class SimpleObjectReference(models.Model):
    model = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)

    # TODO: make this a manager?
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
