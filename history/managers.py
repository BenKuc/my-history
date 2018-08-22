from django.db import models

from history.utils.bulk_create import bulk_create as mt_bulk

# TODO: here hook into methods that need to send a custom signal
# -> TODO: implement event-signals and event models


class ModelQuerySet(models.QuerySet):
    # TODO: if this is tested provide settings option for this to be the
    #       default bulk_create
    def mt_bulk_create(self, objs, batch_size=None):
        return mt_bulk(objs, batch_size)

    def bulk_create(self, objs, batch_size=None):
        # TODO: pre or post?
        return super().bulk_create(objs, batch_size)

    def update(self, **kwargs):
        # TODO: pre or post?
        return super().update(**kwargs)
