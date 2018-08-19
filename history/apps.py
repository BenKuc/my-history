from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import class_prepared, post_save

# from ..receivers import save_receiver
from django.apps.registry import apps

from .history_models.register import create_history_on_models


class HistoryConfig(AppConfig):
    # name = settings.MY_HISTORY['APP_NAME']
    name = 'history'
    verbose_name = settings.MY_HISTORY['VERBOSE_APP_NAME']

    def import_models(self):
        # if this app is set as the last one in INSTALLED_APPS
        # all relevant models are loaded now
        create_history_on_models()
        super().import_models()

    def ready(self):
        # TODO: how to get sender in here? maybe even multiple senders? -> multiple models
        #       post_save.connect(save_receiver, sender=None)
        # TODO: connect all signals to be connected here!
        # TODO: test for duplicated signals
        pass
