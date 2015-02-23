# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from model_utils.models import StatusModel, TimeStampedModel

from djspikeval.models.util import AccessChoices


__all__ = ["Benchmark"]
__author__ = "pmeier82"


class Benchmark(StatusModel, TimeStampedModel):
    """benchmark container class

    A Benchmark represents a set of Trials that belong together, and usually
    originate from the same source. This is a mere container for trials, which
    represent data files.
    """

    # meta
    class Meta:
        app_label = "djspikeval"
        get_latest_by = "modified"

    # choices
    STATUS = AccessChoices

    # fields
    name = models.CharField(
        _("name"),
        max_length=255,
        help_text="The name will be used as an identifier for the Benchmark. "
                  "(character limit: 255)")
    description = models.TextField(
        blank=True,
        help_text="Use this field to give a detailed description of the "
                  "Benchmark. Although there is no limit to the content "
                  "of this field, you may want to provide an attached file "
                  "if your space or editing requirements are not met. "
                  "(character limit: none)")
    parameter = models.CharField(
        max_length=255,
        default="No.",
        help_text="Individual Trials of the Benchmark can have a parameter attached "
                  "that can be used to order and distinguish the Trials. This may "
                  "be a simulation or experimental parameter that has been varied "
                  "systematically or just a numbering (default). "
                  "(character limit: 255)")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=2,
        help_text="The user who contributed this Benchmark.",
        related_name="benchmarks")

    # managers
    tags = TaggableManager(
        _("Benchmark Tags"),
        help_text="A comma-separated list of tags classifying the Benchmark.",
        blank=True)

    # methods
    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return "benchmark:detail", (self.pk,), {}

    @models.permalink
    def get_delete_url(self):
        return "benchmark:delete", (self.pk,), {}

    def is_public(self):
        return self.status == Benchmark.STATUS.public

    def is_editable(self, user):
        return self.owner == user or user.is_superuser

    def is_accessible(self, user):
        return self.is_public() or self.is_editable(user)

    def toggle(self):
        if self.status == Benchmark.STATUS.public:
            self.status = Benchmark.STATUS.private
        else:
            self.status = Benchmark.STATUS.public
        self.save()

    def trial_set_valid(self):
        return self.trial_set.filter(
            ~models.Q(valid_rd_log__contains="ERROR"),
            ~models.Q(valid_gt_log__contains="ERROR"))

    def submission_count(self, user=None):
        return self.batch_set.filter(status__exact="public").count()


if __name__ == "__main__":
    pass
