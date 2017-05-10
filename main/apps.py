from django.apps import AppConfig

from .tasks import consumer


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        consumer.delay()
