# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from djspikeval.signals import spike_evaluation_run, spike_validate_st

__all__ = ["Evaluation"]
__author__ = "pmeier82"


class Evaluation(StatusModel, TimeStampedModel):
    """single trial evaluation object

    When user wants to evaluate the results of his spike sorting work, he
    creates an evaluation. Physically, an evaluation binds together
    user-uploaded file with sorted data, an original version of the raw data
    file and the evaluation results.
    """

    STATUS = Choices("initial", "running", "success", "failure")

    ## meta

    class Meta:
        app_label = "djspikeval"

    ## fields

    task_id = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    task_log = models.TextField(
        blank=True,
        null=True)
    valid_ev_log = models.TextField(
        blank=True,
        null=True)
    batch = models.ForeignKey("djspikeval.Batch")
    trial = models.ForeignKey("djspikeval.Trial")

    ## managers

    datafile_set = GenericRelation("djspikeval.Datafile")

    ## special methods

    def __str__(self):
        return "#%s $%s @%s" % (self.batch_id, self.pk, self.trial_id)

    def __unicode__(self):
        return unicode(self.__str__())

    ## interface

    @property
    def modules(self):
        try:
            return self.trial.benchmark.module_set.filter(enabled=True)
        except:
            return []

    @property
    def ev_file(self):
        try:
            return self.datafile_set.filter(kind="st_file")[0]
        except IndexError:
            return None

    @property
    def is_valid_ev_file(self):
        if not self.valid_gt_log:
            return False
        if self.valid_gt_log.find("ERROR") >= 0:
            return False
        return True

    def processed(self):
        return self.status == self.STATUS.success

    def is_accessible(self, user):
        return self.batch.is_accessible(user)

    def clear_results(self):
        try:
            for res in self.result_set.all():
                res.delete()
                # INFO:
                # dont use bulk delete, as the overloaded delete wont be called!
                # this will leave the files in place, we dont want that
        except:
            pass

    def run(self):
        spike_evaluation_run.send_robust(sender=self)

    def validate(self):
        spike_validate_st.send_robust(sender=self)


if __name__ == "__main__":
    pass
