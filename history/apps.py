from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save

#from ..receivers import save_receiver


verbose_name = settings.DJANGO_HISTORY['app_name']
name = settings.DJANGO_HISTORY['name']


class HistoryConfig(AppConfig):
    name = 'history'
    verbose_name = verbose_name

    def ready(self):
        # TODO: how to get sender in here? maybe even multiple senders? -> multiple models
 #       post_save.connect(save_receiver, sender=None)
        # TODO: connect all signals to be connected here!
        # TODO: test for duplicated signals
        pass
