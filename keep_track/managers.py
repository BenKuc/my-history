import copy

from django.db import models

from keep_track.utils.bulk_create import bulk_create as mt_bulk
from keep_track import signals


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
