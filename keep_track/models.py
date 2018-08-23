from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


__all__ = [
    'ObjectHistory', 'SimpleObjectReference', 'HistoryBaseModel', 'ObjectEvent',
]


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

    # TODO: these need to be added in manager
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


# TODO: we do not want this -> make correct history for all!
class SimpleObjectReference(models.Model):
    model = models.ForeignKey(
        'contenttypes.ContentType', on_delete=models.CASCADE,
    )
    pk_value = models.CharField(max_length=255)
    instance = GenericForeignKey(fk_field='pk_value', ct_field='model')


# TODO: I
class ObjectEvent(models.Model):
    """
    An instance of this always belongs to a ManagerEvent-instance.
    """
    type = models.CharField(
        choices=(
            ('C', 'creation'),
            ('U', 'update'),
            ('D', 'deletion'),
        )
    )
    diff = models.OneToOneField(Diff, on_delete=models.CASCADE, null=True)
    object_history = models.ForeignKey(
        'keep_track.ObjectHistory', related_name='events', on_delete=models.CASCADE,
    )
    history_date = models.DateTimeField(auto_now_add=True)
    before = models.OneToOneField(
        'keep_track.HistoryBaseModel',
        null=True,
        on_delete=models.CASCADE,
        related_name='next_event',
    )
    after = models.OneToOneField(
        'keep_track.HistoryBaseModel',
        null=True,
        on_delete=models.CASCADE,
        related_name='previous_event',
    )

    class Meta:
        order_by = ['+history_data']

    def __str__(self):
        return '{}-event at {}.'.format(self.type, self.history_date)


# TODO: make this abstract?
# TODO: where is the db-link between model and history-model?
# TODO: set correct indexes and order_by to speed up querying
class TrackBase(models.Model):
    composed_pk = models.CharField(
        max_length=255, primary_key=True, unique=True,
    )
    # TODO: model is not required -> the model is implied (see above)
    model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    id = models.CharField(max_length=255)
    # TODO: this is invalid and also reverse relation has to be removed
    #       -> descriptor
    history_object = GenericForeignKey(
        ct_field='model', fk_field='id',
    )
    # TODO: this must be computed -> this is also unnecessary;
    duplication = models.PositiveIntegerField()
    # TODO: this is duplicated data due to history_date
    rank = models.PositiveIntegerField()
    # TODO: add correct kwargs + built in unique_together; history_date is
    #       somehow unique with model and id?
    history_date = models.DateTimeField()

    class Meta:
        # TODO: a track_id does not make sense -> we will never query for that
        unique_together = ('object_pk', 'content_type', 'id', 'rank', )

    # TODO:
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
