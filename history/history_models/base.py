from django.db.models import Model as DjangoModel


# TODO: just include this in the code and put it into installed-apps as: django_history

# TODO: mapping from models to already registered history-models to use tables efficiently


def get_history_fields(model, fields):
    pass
    # TODO: get related models to be processed by history


def get_history_model_name(model_name):
    # TODO: involve app name to avoid conflicts
    pass


def history(fields='__all__', differences=False, db_alias='default', history_model_name=''):
    """

    :param fields: fields that should be tracked
    :param differences: boolean indicating whether differences shall be tracked
    :param db_alias: connection string to the database where the history-table should be created
    :param history_model_name: name of the history model to be used
    :return:
    """
    # TODO: create model that is checked -> do you get the model or the class definition?

    if fields == '__all__':
        fields = []
    assert isinstance(fields, (list, tuple)), "Parameter fields of history decorator must be a list or tuple."

    def create_history_model(ModelClass: DjangoModel):
        # TODO: set custom managers on the ModelClass
        assert isinstance(ModelClass, DjangoModel), "The registered class must be a subtype of django.db.models.Model"

        # ???: This might not work -> when does this code run?
        model_fields = [f for f in ModelClass._meta.get_fields() if f in fields]
        relations = {f.name: f for f in model_fields if f.is_relation}

        registered_models = ModelTracker.objects.select_related('model').all()
        # TODO: follow relations that should be set up exactly the same way -> get reverse relations (lazily?)
        for rel in relations:
            # TODO: check for related_name and if it is in relations!

            # TODO: register all of them in the db?
            if rel.related_model in registered_models:
                pass
            else:
                # TODO: create sub history_model and register it
                pass

        # TODO: register and create the main model here
        # TODO: how to set which app it belongs to?
        history_model = type(history_model_name, (DjangoModel,), dict={})

    return create_history_model


# TODO: handle different inheritance structures comming with Python (multi-table-inheritance)
