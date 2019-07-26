from django.apps import AppConfig


class ScrapydDashConfig(AppConfig):
    name = 'scrapyd_dash'
    verbose_name = "Scrapyd Dashboard"

    def ready(self):
        from .utils import updater
        updater.start_updater()