# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from .datafile import Datafile
from .submission import Submission
from ..signals import spike_analysis, spike_validation_st


__all__ = ["Analysis"]
__author__ = "pmeier82"


class Analysis(StatusModel, TimeStampedModel):
    """single datafile analysis object

    When a user wants to evaluate the results of his spike sorting work, he
    creates an analysis. Physically, an analysis binds together
    user-uploaded file with sorted data, an original version of the raw data
    file and the analysis results.
    """

    # meta
    class Meta:
        app_label = "djspikeval"
        get_latest_by = "modified"
        order_with_respect_to = "datafile"

    # choices
    STATUS = Choices("initial", "running", "success", "failure")

    # fields
    task_id = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    task_log = models.TextField(
        blank=True,
        null=True)
    valid_st_log = models.TextField(
        blank=True,
        null=True)
    submission = models.ForeignKey(Submission)
    datafile = models.ForeignKey(Datafile)

    # managers
    asset_set = GenericRelation("base.Asset")

    @property
    def st_file(self):
        try:
            return self.asset_set.filter(kind="st_file")[0]
        except IndexError:
            return None

    # methods
    def __unicode__(self):
        return unicode("Analysis #{}: {} << {}".format(self.pk, self.datafile, self.submission.algorithm))

    @property
    def modules(self):
        try:
            return self.datafile.dataset.module_set.filter(enabled=True)
        except:
            return []

    @property
    def is_valid_st_file(self):
        if not self.valid_st_log:
            return False
        if self.valid_st_log.find("ERROR") >= 0:
            return False
        return True

    def processed(self):
        return self.status == self.STATUS.success

    def is_accessible(self, user):
        return self.submission.is_accessible(user)

    def clear_results(self):
        try:
            for res in self.result_set.all():
                res.delete()
                # INFO:
                # dont use bulk delete, as the overloaded delete wont be called!
                # this will leave the files in place, we dont want that
        except:
            pass

    def start(self):
        spike_analysis.send_robust(sender=self)

    def validate(self):
        spike_validation_st.send_robust(sender=self)


if __name__ == "__main__":
    pass
