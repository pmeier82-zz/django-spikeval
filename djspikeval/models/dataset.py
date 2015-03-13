# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from model_utils.models import StatusModel, TimeStampedModel

from djspikeval.models.util import AccessChoices


__all__ = ["Dataset"]
__author__ = "pmeier82"


class Dataset(StatusModel, TimeStampedModel):
    """dataset container class

    A `Dataset` represents a set of ``Datafile`s that belong together.
    This is mostly a container for `Datafile`s.
    """

    # meta
    class Meta:
        app_label = "djspikeval"
        get_latest_by = "modified"
        ordering = ("-modified", "name")

    # choices
    STATUS = AccessChoices

    # fields
    name = models.CharField(
        _("name"),
        max_length=255,
        help_text="The name will be used as an identifier for the Dataset. "
                  "(character limit: 255)")
    description = models.TextField(
        blank=True,
        help_text="Use this field to give a detailed description of the "
                  "Dataset. Although there is no limit to the content "
                  "of this field, you may want to provide an attached file "
                  "if your space or editing requirements are not met. "
                  "(character limit: none)")
    parameter = models.CharField(
        max_length=255,
        default="No.",
        help_text="Individual datafiles of the dataset can have a parameter attached "
                  "that can be used to order and distinguish the datafiles. This may "
                  "be a simulation or experimental parameter that has been varied "
                  "systematically or just a numbering (default). "
                  "(character limit: 255)")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=2,
        help_text="The user who contributed this dataset.")

    # managers
    kind = TaggableManager(
        _("Dataset Kind"),
        help_text="A comma-separated list of tags classifying the Dataset.",
        blank=True)
    asset_set = GenericRelation("base.Asset")

    @property
    def attachment_set(self):
        return self.asset_set.filter(kind="attachment")

    # methods
    def __unicode__(self):
        return unicode("Dataset: {}".format(self.name))

    @models.permalink
    def get_absolute_url(self):
        return "dataset:detail", (self.pk,), {}

    @models.permalink
    def get_delete_url(self):
        return "dataset:delete", (self.pk,), {}

    def is_public(self):
        return self.status == Dataset.STATUS.public

    def is_editable(self, user):
        return self.user == user or getattr(user, "is_superuser", False) is True

    def is_accessible(self, user):
        return self.is_public() or self.is_editable(user)

    def toggle(self):
        if self.status == Dataset.STATUS.public:
            self.status = Dataset.STATUS.private
        else:
            self.status = Dataset.STATUS.public
        self.save()

    def datafile_set_valid(self):
        return self.datafile_set.filter(
            ~models.Q(valid_rd_log__contains="ERROR"),
            ~models.Q(valid_gt_log__contains="ERROR"))

    def submission_count(self, user=None):
        try:
            if user.is_superuser():
                return self.submission_set.count()
            return self.submission_set.filter(
                models.Q(status__exact="public") |
                models.Q(owner_id=user.pk)
            ).count()
        except:
            return self.submission_set.filter(status__exact="public").count()


if __name__ == "__main__":
    pass
