from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompetitionConfig(AppConfig):
    name = "talana_prueba.competition"
    verbose_name = _("Competition")

    def ready(self):
        try:
            import talana_prueba.competition.signals  # noqa F401
        except ImportError:
            pass
