import itertools

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import signals as django_signals

from .events import receivers, signals
from .managers import ModelQuerySet
from history.common.validation import (
    assert_iterable, assert_three_tuple_iterable,
)


TRACKED_MODELS = set()


def get_history_name(model):
    scheme = settings.MY_HISTORY.MODEL_NAMING_SCHEME
    return scheme.format(name=model.__name__)


class History:

    def __init__(self, fields='__all__', track_diffs=False,
                 extra_fields=None, exclude_fields=None):
        """

        Args:
            fields: fields that should be tracked
            track_diffs: boolean indicating whether differences
                         shall be tracked
            extra_fields: This is a list of 3-tuples for tracking extra stuff
                             (
                                name: str,
                                field: django.db.models.Field,
                                val: method or value,
                             )
            exclude_fields: Fields to be excluded from tracking, because default
                            is __all__.
        """
        self.fields = fields
        self.track_diffs = track_diffs

        if exclude_fields is None:
            exclude_fields = {}
        assert_iterable('exclude_fields', exclude_fields)
        self.exclude_fields = exclude_fields

        global_extra_fields = settings.MY_HISTORY['GLOBAL_EXTRA_FIELDS']
        assert_three_tuple_iterable('global_extra_fields', global_extra_fields)
        assert_three_tuple_iterable('extra_fields', extra_fields)

        self.extra_fields = list(
            itertools.chain(extra_fields, global_extra_fields)
        )

    def contribute_to_class(self, cls, name):
        """
        This sets all the history methods, managers and wrappers on the regarded
        model that are required for the history to work.

        Args:
            cls: The model class on which History is set.
            name: The attribute-name of the History-instance.
        """
        self.model = cls
        TRACKED_MODELS.add(self.model)

        django_signals.class_prepared.connect(
            self.create_history_model, sender=self.model,
        )

        # wrappers around methods to connect to history
        setattr(cls, 'objects', ModelQuerySet.as_manager())
        setattr(
            cls, name, GenericRelation(
                'history.ObjectHistory', related_name=cls.__name__,
            ),
        )

    def create_history_model(self, sender, **kwargs):
        """
        Returns:
            The history model for the corresponding self.model.
            This method is connected via class_prepared signal.
        """
        history_model = type(
            get_history_name(self.model),
            bases=self.get_bases(),
            dict=self.get_dict(),
        )

        # set history manager: we couldn't do this in contribute_to_class
        #                      as it didn't exist at this point
        manager_name = settings.MY_HISTORY['MODEL_HISTORY_NAME']
        setattr(sender, manager_name, history_model.objects)

        django_signals.post_save.connect(receivers.save_receiver, sender=sender)
        django_signals.post_delete.connect(receivers.delete_receiver, sender=sender)
        signals.post_update.connect(receivers.update_receiver, sender=sender)
        signals.post_bulk_create.connect(receivers.bulk_create_receiver, sender=sender)
        signals.post_mt_bulk_create.connect(receivers.mt_bulk_create_receiver, sender=sender)

        return history_model

    def get_bases(self):
        # TODO E1a
        for b in self.model.mro():
            pass
        return (models.Model, )

    def get_dict(self):
        # TODO E1c
        #if self.fields == '__all__':
         #   self.fields = []
        #assert isinstance(fields, (list, tuple)), ERROR_MESSAGES['TYPE_FIELDS']

        history_dict = {}
        history_dict.update(self.get_fields())

        class Meta:
            pass

        for key, val in self.get_meta_options():
            setattr(Meta, key, val)

        history_dict.update({'Meta': Meta})

        return history_dict

    def get_fields(self):
        opts = self.model._meta
        history_fields = {}

        # TODO E1b

        # 1) FK and OneToOne
        for f in opts.fields:
            if f.is_relation:
                pass
            else:
                pass

        # 2) Many-to-Many
        for m2m in opts.many_to_many:
            pass

        # 3) One-To-Many (is this necessary??) -> yes, setting it up +
        #    reverse-relations and reverse one-to-one?
        for rel in opts.related_objects:
            pass

        for f in self.config.extra_fields:
            pass

        return history_fields

    def get_meta_options(self):
        # TODO E1d
        # app_label = settings.MY_HISTORY.APP_NAME
        options = {'app_label': 'history'}
        return options

