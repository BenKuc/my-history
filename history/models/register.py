from collections import namedtuple
import inspect

from django.conf import settings
from  django.core.exceptions import ImproperlyConfigured
from django.db import models

from myhistory.settings_history import GLOBAL_TRACK_FIELDS
from .constants import ERROR_MESSAGES
from .models import HistoryQuerySet, ModelQuerySet, GenericRelation


HistoryConfig = namedtuple(
    typename='HistoryConfig',
    field_names='field_names extra_fields track_diffs',
)


TRACKED_MODELS = {}


# TODO: actually we want to modify the model-class before it is given to
#       the django meta-class! -> look into order of statements
def history(fields='__all__', track_diffs=False, extra_fields=None):
    """
    :param fields: fields that should be tracked
    :param track_diffs: boolean indicating whether differences shall be tracked
    :param extra_fields: This is a list of 3-tuples for tracking extra stuff
                         (name: str, field: django.db.models.Field,
                          val: method or value)
    """

    if fields == '__all__':
        fields = []
    assert isinstance(fields, (list, tuple)), ERROR_MESSAGES['TYPE_FIELDS']

    extra = extra_fields + GLOBAL_TRACK_FIELDS
    for _, field, method in extra.copy():
        if not isinstance(field, models.Field):
            # TODO: django-check as error -> for not valid fields
            raise ImproperlyConfigured()
        sig = inspect.signature(method)
        # TODO: add correct error messages
        assert set(sig.parameters.keys()) == {'instance', 'request'}, ""
        assert sig.parameters['instance'].kind == inspect.Parameter.POSITIONAL_ONLY, ""
        assert sig.parameters['request'].kind == inspect.Parameter.POSITIONAL_ONLY, ""

    def set_history_on_model(model):
        assert issubclass(model, models.Model), ERROR_MESSAGES['TYPE_MODEL']
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

    return set_history_on_model


def create_history_on_models():
    for model_cls, config in TRACKED_MODELS.items():
        creator = HistoryCreator(model_cls, config)
        creator.create_history()


class HistoryCreator:

    def __init__(self, model_cls, config):
        self.model = model_cls
        self.config = config

    def create_history(self):
        scheme = settings.MY_HISTORY.MODEL_NAMING_SCHEME
        name = scheme.format(name=self.model.__name__)

        bases = self.get_bases()

        # app_label = settings.MY_HISTORY.APP_NAME

        history_dict = self.get_dict()

        # TODO: get correct bases -> multi-table inheritance
        type(name, bases, dict=history_dict)

    def get_bases(self):
        # TODO: do this correctly (also multi-table inheritance)
        for b in self.model.mro():
            pass

    def get_dict(self):
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
        options = {'app_label': 'history'}
        # TODO: look into django-model Meta docs
        # TODO: db_table_name!
        return options
