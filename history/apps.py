from django.apps import AppConfig
from django.conf import settings

# from ..receivers import save_receiver

from history.models.register import create_history_on_models


class HistoryConfig(AppConfig):
    name = 'history'
    verbose_name = settings.MY_HISTORY['VERBOSE_APP_NAME']

    def import_models(self):
        # if this app is set as the last one in INSTALLED_APPS
        # all relevant models are loaded now
        create_history_on_models()
        super().import_models()

    def ready(self):
        pass
