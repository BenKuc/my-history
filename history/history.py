import inspect
import itertools

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import class_prepared

from .managers import HistoryQuerySet, ModelQuerySet
from .constants import (
    DEFAULT_ITERABLES, HISTORY_ERROR_MESSAGES, EXTRA_FIELDS_SIGNATURE,
)


TRACKED_MODELS = set()


def assert_iterable(name, obj):
    base_msg = HISTORY_ERROR_MESSAGES['DEFAULT_ITERABLES']
    msg = base_msg.format(name, DEFAULT_ITERABLES)
    assert isinstance(obj, DEFAULT_ITERABLES), msg


def assert_correct_three_tuple(name, field, value):
    errors = []
    if not isinstance(name, str):
        errors.append(HISTORY_ERROR_MESSAGES['NAME_STRING'])
    if not isinstance(field, models.Field):
        errors.append(HISTORY_ERROR_MESSAGES['FIELD_DJANGO'])

    if callable(value):
        sig = inspect.signature(value)
        if not set(sig.parameters.keys()) == EXTRA_FIELDS_SIGNATURE:
            errors.append(HISTORY_ERROR_MESSAGES['WRONG_SIGNATURE'])
    return errors


def get_history_name(model):
    scheme = settings.MY_HISTORY.MODEL_NAMING_SCHEME
    return scheme.format(name=model.__name__)


def assert_three_tuple_iterable(name, obj):
    assert_iterable(name, obj)

    errors = []
    for idx, element in enumerate(obj):
        idx_errors = []
        if not isinstance(element, tuple):
            idx_errors.append(HISTORY_ERROR_MESSAGES['TUPLE_REQUIRED'])
        elif len(element) == 3:
            idx_errors.append(HISTORY_ERROR_MESSAGES['LENGTH_THREE'])
        else:
            idx_errors.append(assert_correct_three_tuple(element))
        if idx_errors:
            errors.append(
                "Error on index {}: {}".format(idx, ' '.join(idx_errors))
            )

    assert not errors, HISTORY_ERROR_MESSAGES['EXTRA_FIELDS_ERROR'].format(
        name, ' & '.join(errors))


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

        class_prepared.connect(self.create_history_model, sender=self.model)

        # wrappers around methods to connect to history
        setattr(cls, 'objects', ModelQuerySet.as_manager())
        # set history manager
        manager_name = settings.MY_HISTORY['MODEL_HISTORY_NAME']
        setattr(cls, manager_name, HistoryQuerySet.as_manager())
        setattr(
            cls, name, GenericRelation(
                'history.ObjectHistory', related_name='original',
            ),
        )

    def create_history_model(self):
        """
        Returns:
            The history model for the corresponding self.model.
            This method is connected via class_prepared signal.
        """
        return type(
            get_history_name(self.model),
            bases=self.get_bases(),
            dict=self.get_dict(),
        )

    def get_bases(self):
        # TODO: do this correctly (also multi-table inheritance)
        for b in self.model.mro():
            pass
        return (models.Model, )

    def get_dict(self):
        # TODO: combine this with the below also using TRACKED_MODELS
        #if fields == '__all__':
           # # TODO: these must be included
          #  # TODO: consider exclude_fields
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

        # TODO: think fo all cases here: also reverse one-to-one and
        #       multi-table-inheritance -> set custom bulk_create e.g.

        # TODO: set correct references: history.HistoryModel/SimpleReference
        #       depending on whether related_model in TRACKED_MODELS

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
        # app_label = settings.MY_HISTORY.APP_NAME
        options = {'app_label': 'history'}
        # TODO: look into django-model Meta docs
        # TODO: db_table_name!
        return options

