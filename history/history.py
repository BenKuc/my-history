import inspect
import itertools

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from .models.constants import ERROR_MESSAGES


class History:

    def __init__(self, fields='__all__', track_diffs=False, extra_fields=None, exclude_fields=None):
        """
        :param fields: fields that should be tracked
        :param track_diffs: boolean indicating whether differences shall be tracked
        :param extra_fields: This is a list of 3-tuples for tracking extra stuff
                             (name: str, field: django.db.models.Field,
                              val: method or value)
        """

        if fields == '__all__':
            # TODO: these must be included
            # TODO: consider exclude_fields
            fields = []
        assert isinstance(fields, (list, tuple)), ERROR_MESSAGES['TYPE_FIELDS']

        global_extra_fields = settings.MY_HISTORY['GLOBAL_EXTRA_FIELDS']
        extra_fields = list(itertools.chain(extra_fields, global_extra_fields))

        for _, field, method in extra_fields:
            if not isinstance(field, models.Field):
                # TODO: django-check as error -> for not valid fields
                raise ImproperlyConfigured()

            sig = inspect.signature(method)
            # TODO: add correct error messages -> Django-check
            assert set(sig.parameters.keys()) == {'instance', 'request'}, ""
            only_pos = inspect.Parameter.POSITIONAL_ONLY
            assert sig.parameters['instance'].kind == only_pos, ""
            assert sig.parameters['request'].kind == only_pos, ""

        # TODO: put this to somewhere else! -> contribute_to_class
        if model not in TRACKED_MODELS:
            TRACKED_MODELS[model] = HistoryConfig(
                field_names=fields,
                extra_fields=extra_fields,
                track_diffs=track_diffs,
            )

        # TODO: wrap methods that need to send a signal
        #        -> (QuerySet.update/bulk_create)
        # set overwritten manager
        setattr(model, 'objects', ModelQuerySet.as_manager())

        # set history manager
        # TODO: get name from settings
        setattr(model, 'history_objects', HistoryQuerySet.as_manager())

        # TODO: this might not be possible (test + see comment above!)
        # set extra relation
        # TODO: related_query_name?
        # TODO: get name from settings
        # TODO: set this correctly
        setattr(model, 'history', GenericRelation())
        return model

    def contribute_to_class(self, cls, name):
        # TODO: implement! must important
        pass
