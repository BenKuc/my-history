from collections import namedtuple, OrderedDict

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


class HistoryDispatcher:
    # key: model, value: list of other models the history of key depends on
    dependencies = {}
    # key: number of dependencies, value: list of models with that number
    buckets = OrderedDict()

    def __init__(self):
        pass

    def __init__(self):
        # TODO: this is unnecessary: if it is in tracked_models then ok,
        #       otherwise set foreignkey to basic history model!
        # TODO: implement algorithm of dependency check -> django check
        for model_cls, config in TRACKED_MODELS.items():
            self.dependencies[model_cls] = self.get_dependencies(model_cls)

    def get_dependencies(self, model_cls):
        # TODO: this is flat dependencies!!!
        if model_cls not in self.dependencies:
            dependencies = set()
            self.dependencies[model_cls] = dependencies
        return self.dependencies[model_cls]


# TODO: put this to HistoryDispatcher
class HistoryCreator:

    def __init__(self, model_class, **kwargs):
        import pdb; pdb.set_trace()
        self.model_cls = model_class
        self.config = TRACKED_MODELS[model_class]

        dependencies = self.get_dependencies()
        left_dependencies = dependencies.difference(self.READY_MODELS)

        if left_dependencies:
            for model in left_dependencies:
                # TODO: register and then do it directly???
                pass
        else:
            pass

        # TODO: maybe get this another way
        relations = [f for f in model_class._meta.get_fields() if f.is_relation]
        for rel in relations:
            # TODO: for reverse relations: reverse dependecy
            rel_model = rel.related_model
            # TODO: what to do with models that are not registered? ->
            # simple history -> register simple history
            # (generic-fk to the model instance)
            # class_prepared.connect(receiver=cre)

        # register related_models recursively -> NO! check

        # TODO: get fields and related-history-models. ->
        #  TODO: also connect sub-stuff to class_prepared!
        # TODO: get history-name by scheme of settings.
        # TODO: Meta-class -> db_table name! and app_label!.
        # TODO: custom managers on cls!

    def register_simple_history(self):
        pass

    def register_history(self):
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
