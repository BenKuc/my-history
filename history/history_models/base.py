from django.conf import settings
from django.db import models

# TODO: move these to constants
# TODO: more information by model-cls and so on
ERROR_TYPE_FIELDS = "Parameter fields of history decorator " \
                    "must be a list or tuple."
ERROR_TYPE_MODEL = "The registered class must be a subtype of " \
                   "django.db.models.Model"


def get_history_model_name(model):
    scheme = settings.MY_HISTORY.MODEL_NAMING_SCHEME
    return scheme.format(name=model.__name__)


def get_app_label():
    return settings.MY_HISTORY.APP_NAME


def get_history_model_dict(model, fields):
    # TODO: get related models to be processed by history
    history_dict = {}
    return history_dict


def get_model_meta_dict(model):
    pass


def history(fields='__all__', differences=False):
    """
    :param fields: fields that should be tracked
    :param differences: boolean indicating whether differences shall be tracked
    """

    if fields == '__all__':
        fields = []
    assert isinstance(fields, (list, tuple)), ERROR_TYPE_FIELDS

    # TODO: get fields and related-history-models -> make Queue!
    # TODO: get history-name by scheme of settings
    # TODO: Meta-class -> db_table name! and app_label!
    # TODO: custom managers on cls!

    def create_history_model(model):
        assert isinstance(model, models.Model), ERROR_TYPE_MODEL

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
            bases=(models.Model, ),
            dict=get_history_model_dict(model),
        )

    return create_history_model
