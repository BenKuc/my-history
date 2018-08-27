import copy

from django.db import models

from keep_track.utils.bulk_create import bulk_create as mt_bulk
from keep_track import signals


__all__ = [
    'TrackDescriptor', 'TrackManager', 'InstanceTrackManager',
]


class TrackDescriptor:

    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner):
        assert owner == self.model, "Can this happen at all?"
        if instance is not None:
            return InstanceTrackManager(model=owner, instance=instance)
        else:
            return TrackManager(model=owner)


class ModelQuerySet(models.QuerySet):
    def mt_bulk_create(self, objs, batch_size=None):
        res = mt_bulk(objs, batch_size)
        signals.post_mt_bulk_create.send(
            self.model,
            ids=res,
            objs=objs,
            batch_size=batch_size,
        )
        return res

    def bulk_create(self, objs, batch_size=None):
        res = super().bulk_create(objs, batch_size)
        signals.post_bulk_create.send(
            self.model,
            ids=res,
            objs=objs,
            batch_size=batch_size,
        )
        return res

    def update(self, **kwargs):
        res = super().update(**kwargs)
        signals.post_update(
            self.model,
            queryset=copy.copy(self),
            update_kwargs=kwargs,
        )
        return res


class TrackManager(models.Manager):

    def __init__(self, model):
        self.model = model
        super().__init__()

    def get_queryset(self):
        return super().get_queryset().select_related('event')

    def event_type(self, type_):
        return self.get_queryset().selected_related(
            'event',
        ).filter(
            event__type=type_,
        )

    def updates(self):
        return self.event_type('U')

    def creations(self):
        return self.event_type('C')

    def deletions(self):
        return self.event_type('D')


class InstanceTrackManager(TrackManager):

    def __init__(self, model, instance):
        self.instance = instance
        super().__init__(model)

    # this is sufficient as all methods on TrackManager call .get_queryset()
    def get_queryset(self):
        pk_field = self.model._meta.get_field('pk')
        pk_key = pk_field.name

        if pk_field.is_relation:
            pk_key += '_id'

        look_up = {pk_key: getattr(self.instance, pk_key)}
        return super().get_queryset().filter(**look_up)

    # TODO: naming problem: it is still creations and deletions here


# TODO: implement!
class EventManager(models.Manager):

    def __init__(self, model):
        self.model = model
        super().__init__()


# TODO: implement!
class InstanceEventManager(EventManager):
    pass
