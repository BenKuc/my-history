from django.db import models
from django.utils import timezone


__all__ = [
    'EventBase', 'TrackBase', 'TrackModelRelation',
]


# TODO: this must be added dynamically to TrackModel + to model dynamically
event = models.OneToOneField('keep_track.Event', related_name='state')
# TODO: add pk-field for the model (specific)
# TODO: I
class EventBase(models.Model):
    type = models.CharField(
        choices=(
            ('C', 'creation'),
            ('U', 'update'),
            ('D', 'deletion'),
        )
    )
    track_date = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['+track_date']
        abstract = True

    def __str__(self):
        return '{}-event at {}.'.format(self.type, self.track_date)

    @property
    def previous(self):
        state_pk_name = self.__class__._meta.get_field('state').related_model.pk.name
        state_pk_val = self.state.pk
        # TODO: use F()-expressions here: F('track_date')
        look_up = {
            state_pk_name: state_pk_val, 'track_date__lte': self.track_date,
        }
        return self.__class__.objects.filter(**look_up).last()

    @property
    def next(self):
        state_pk_name = self.__class__._meta.get_field(
            'state').related_model.pk.name
        state_pk_val = self.state.pk
        # TODO: use F()-expressions here: F('track_date')
        look_up = {
            state_pk_name: state_pk_val, 'track_date__gte': self.track_date,
        }
        return self.__class__.objects.filter(**look_up).first()


class TrackBase(models.Model):

    class Meta:
        abstract = True
        # TODO: set dynamically
        order_with_respect_to = 'Event'

    @property
    def previous(self):
        pk_name = self.__class__._meta.pk.name
        # TODO: use F()-expressions here: F('event__track_date')
        look_up = {
            pk_name: self.pk, 'event__track_date__lte': self.event.track_date,
        }
        return self.__class__.objects.filter(**look_up).last()

    @property
    def next(self):
        pk_name = self.__class__._meta.pk.name
        # TODO: use F()-expressions here: F('event__track_date')
        look_up = {
            pk_name: self.pk, 'event__track_date__gte': self.event.track_date,
        }
        return self.__class__.objects.filter(**look_up).last()


# TODO: use this for migrations and stuff like that
# TODO: use in history.py -> bulk_create!
class TrackModelRelation:
    model = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.CASCADE,
        related_name='track_model',
    )
    track_model = model.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.CASCADE,
        related_name='track_model',
        unique=True,
    )
