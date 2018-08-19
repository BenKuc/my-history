from collections import namedtuple

from django.conf import settings
from django.db import models

# TODO: move these to constants
# TODO: more information by model-cls and so on
ERROR_TYPE_FIELDS = "Parameter fields of history decorator " \
                    "must be a list or tuple."
ERROR_TYPE_MODEL = "The registered class must be a subtype of " \
                   "django.db.models.Model"

HistoryConfig = namedtuple(
    typename='HistoryConfig',
    field_names='field_names extra_fields track_diffs',
)

TRACKED_MODELS = {}


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
    assert isinstance(fields, (list, tuple)), ERROR_TYPE_FIELDS

    # TODO: inspect those + add global_extra_fields -> django-checks?
    if extra_fields:
        pass

    def set_history_on_model(model):
        assert issubclass(model, models.Model), ERROR_TYPE_MODEL
        if model not in TRACKED_MODELS:
            TRACKED_MODELS[model] = HistoryConfig(
                field_names=fields,
                extra_fields=extra_fields,
                track_diffs=track_diffs,
            )
        # TODO: set history managers and set history on model-objects
        # TODO: wrap methods that need to send a signal
        #       (QuerySet.update/bulk_create)
        return model

    return set_history_on_model


# TODO: get fields and related-history-models. ->
    #  TODO: also connect sub-stuff to class_prepared!
    # TODO: get history-name by scheme of settings.
    # TODO: Meta-class -> db_table name! and app_label!.
    # TODO: custom managers on cls!
def create_history_on_models():
    # TODO: this needs to be sorted though -> so you can use all of them
    # TODO: do this by the hand
    for model_cls, config in TRACKED_MODELS.items():
        opts = model_cls._meta

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


def get_history_fields():
    pass


def get_meta_options():
    pass


def get_history_model_name(model):
    scheme = settings.MY_HISTORY.MODEL_NAMING_SCHEME
    return scheme.format(name=model.__name__)


def get_app_label():
    return settings.MY_HISTORY.APP_NAME


def get_history_model_dict(model, field_names, extra_fields):
    # TODO: get related models to be processed by history
    # TODO: integrate global_extra_fields from settings!
    history_dict = {}

    # ???: do we need the class to be prepared here?
    # TODO: connect to class_prepared for each one of it
    # TODO: also make a centralized place where duplicate registries are
    #       prevented (because of following relations)
    model_fields = [f for f in model._meta.get_fields() if f.name in fields]
    relations = {f.name: f for f in model_fields if f.is_relation}

    # TODO: follow relations that should be set up exactly the same way
    for rel in relations:
        # TODO: check for related_name and if it is in relations!
        # TODO: create sub_history_models
        pass

    # TODO: register and create the main model here
    # TODO: how to set which app it belongs to?

    # TODO: get correct bases -> multi-table inheritance
    type(
        name=get_history_model_name(model),
        bases=(models.Model,),
        dict=get_history_model_dict(model, extra_fields, field_names),
    )

    return history_dict


def get_model_meta_dict(model):
    # TODO: set app_label here
    pass
