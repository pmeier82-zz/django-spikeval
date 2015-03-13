# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from model_utils.managers import InheritanceManager

__all__ = ["Result"]


class Result(TimeStampedModel):
    """djspikeval result

    module result base class
    """

    # meta
    class Meta:
        app_label = "djspikeval"

    # fields
    analysis = models.ForeignKey('djspikeval.Analysis')
    module = models.ForeignKey("djspikeval.Module")

    # managers
    objects = InheritanceManager()

    # interface
    @property
    def trial(self):
        try:
            return self.analysis.trial
        except:
            return None

    @property
    def batch(self):
        try:
            return self.analysis.submission
        except:
            return None

    @property
    def benchmark(self):
        try:
            return self.analysis.trial.benchmark
            # return self.analysis.batch.dataset
        except:
            return None


if __name__ == "__main__":
    pass
