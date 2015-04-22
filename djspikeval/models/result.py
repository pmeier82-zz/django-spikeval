# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from model_utils.managers import InheritanceManager
from .analysis import Analysis
from .module import Module

__all__ = ["Result"]


class Result(TimeStampedModel):
    """djspikeval result

    module result base class
    """

    # meta
    class Meta:
        app_label = "djspikeval"

    # fields
    analysis = models.ForeignKey(Analysis)
    module = models.ForeignKey(Module)

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
    def submission(self):
        try:
            return self.analysis.submission
        except:
            return None

    @property
    def dataset(self):
        try:
            return self.analysis.trial.dataset
            # return self.analysis.batch.dataset
        except:
            return None


if __name__ == "__main__":
    pass
