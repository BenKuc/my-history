from django.apps import AppConfig
from django.conf import settings


class HistoryConfig(AppConfig):
    name = 'keep_track'
    verbose_name = settings.MY_HISTORY['VERBOSE_APP_NAME']

    def import_models(self):
        # TODO: necessary? -> create history models here by TRACKED_MODELS
        # if this app is set as the last one in INSTALLED_APPS
        # all relevant models are loaded now
        super().import_models()
