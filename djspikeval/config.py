# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjSpikevalAppConfig(AppConfig):
    label = "djspikeval"
    name = "djspikeval"
    verbose_name = _("Django Spikeval")

    def ready(self):
        # import all parts of the application that need to be exposed
        import djspikeval.signals
        import djspikeval.tasks
