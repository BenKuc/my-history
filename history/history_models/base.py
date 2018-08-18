from django.conf import settings
from django.db import models
from django.db.models.signals import class_prepared

# TODO: move these to constants
# TODO: more information by model-cls and so on
ERROR_TYPE_FIELDS = "Parameter fields of history decorator " \
                    "must be a list or tuple."
ERROR_TYPE_MODEL = "The registered class must be a subtype of " \
                   "django.db.models.Model"


TRACKED_MODELS = {}


def history(fields='__all__', track_diffs=False, extra_fields=None):
    """
    :param fields: fields that should be tracked
    :param track_diffs: boolean indicating whether differences shall be tracked
    :param extra_fields: This is a list of 3-tuples for tracking extra stuff
                         (name: str, field: django.db.models.Field,
                          val: method or value)
    """

    model_config = {}

    if fields == '__all__':
        fields = []
    assert isinstance(fields, (list, tuple)), ERROR_TYPE_FIELDS

    # TODO: inspect those + add global_extra_fields
    if extra_fields:
        pass

    model_config['field_names'] = fields
    model_config['extra_fields'] = extra_fields
    model_config['track_diffs'] = track_diffs

    def set_history_on_model(model):
        assert isinstance(model, models.Model), ERROR_TYPE_MODEL

        if model not in TRACKED_MODELS:
            TRACKED_MODELS[model] = model_config
            class_prepared.connect(receiver=create_history_model, sender=model)
        # TODO: set history managers before and set history on model-objects
        return model

    return set_history_on_model


def create_history_model(model_class):
    # TODO: get fields and related-history-models.
    # TODO: get history-name by scheme of settings.
    # TODO: Meta-class -> db_table name! and app_label!.
    # TODO: custom managers on cls!
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
        dict=get_history_model_dict(model),
    )

    return history_dict


def get_model_meta_dict(model):
    # TODO: set app_label here
    pass
