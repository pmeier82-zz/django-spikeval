# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import Choices

from .dataset import Dataset
from ..signals import spike_validation_st, spike_validation_rd


__all__ = ["Datafile"]
__author__ = "pmeier82"


class Datafile(TimeStampedModel):
    """datafile, part of a dataset

    This represents a single set of extracellular data and ground truth
    that a spike-sorting algorithm can be applied on.

    A `Datafile` consists of raw data and (if applicable) the corresponding
    ground truth for that raw data. Data and ground truth are stored in
    separate files.
    Raw data is generally accessible to the public, while the ground
    truth is usually inaccessible to the public, but can be flagged
    as available to the public.

    Raw data is stored in hdf5 format, ground truth is stored in gdf format.
    """

    # meta
    class Meta:
        app_label = "djspikeval"
        unique_together = ("dataset", "parameter")
        ordering = ["dataset", "-parameter"]
        # TODO: does this really make sense?

    # choices
    GT_TYPE = Choices("total", "partial", "none")
    GT_ACCESS = Choices("private", "public")

    # fields
    name = models.CharField(
        max_length=255,
        help_text="The name will be used as an identifier for the Datafile. "
                  "(character limit: 255)")
    description = models.TextField(
        blank=True,
        help_text="Use this field to give a detailed description of the "
                  "Dataset. Although there is no limit to the content "
                  "of this field, you may want to provide an attached file "
                  "if your space or editing requirements are not met. "
                  "(character limit: none)")
    parameter = models.FloatField(
        default=0.0,
        help_text="The parameter value for this Datafile. (type: float)")
    valid_rd_log = models.TextField(
        blank=True,
        null=True)
    valid_gt_log = models.TextField(
        blank=True,
        null=True)
    gt_type = models.CharField(
        choices=GT_TYPE,
        default=GT_TYPE.total,
        max_length=20,
        help_text="Type of ground truth for this Datafile.\n"
                  "Total: all events are explained;\n"
                  "Partial: some events are explained, there may or may not "
                  "be additional events not detailed in the ground truth;\n"
                  "None: no ground truth is provided;")
    gt_access = models.CharField(
        choices=GT_ACCESS,
        default=GT_ACCESS.private,
        max_length=20,
        help_text="Access mode for the ground truth files if provided.")
    dataset = models.ForeignKey(
        Dataset,
        help_text="The Dataset associated with this Datafile.")

    # managers
    asset_set = GenericRelation("base.Asset")

    @property
    def file_set(self):
        return self.asset_set.filter(kind__in=["rd_file", "st_file"])

    # methods
    def __unicode__(self):
        return unicode("Datafile: {}".format(self.name))

    @models.permalink
    def get_absolute_url(self):
        return "datafile:detail", (self.pk,), {}

    @models.permalink
    def get_delete_url(self):
        return "datafile:delete", (self.pk,), {}

    @models.permalink
    def get_validate_url(self):
        return "datafile:validate", (self.pk,), {}

    @property
    def rd_file(self):
        try:
            return self.file_set.filter(kind="rd_file")[0]
        except IndexError:
            return None

    @property
    def is_valid_rd_file(self):
        if not self.rd_file:
            return False
        if not self.valid_rd_log:
            return False
        if self.valid_rd_log.find("ERROR") >= 0:
            return False
        return True

    @property
    def gt_file(self):
        try:
            return self.asset_set.filter(kind="st_file")[0]
        except IndexError:
            return None

    @property
    def is_valid_gt_file(self):
        if self.gt_type == self.GT_TYPE.none:
            return True
        if not self.gt_file:
            return False
        if not self.valid_gt_log:
            return False
        if self.valid_gt_log.find("ERROR") >= 0:
            return False
        return True

    @property
    def gt_public(self):
        return self.gt_access == self.GT_ACCESS.public

    @property
    def is_valid(self):
        return self.is_valid_rd_file and self.is_valid_gt_file

    def validate(self):
        if self.rd_file:
            spike_validation_rd.send_robust(sender=self)
        if self.gt_file:
            spike_validation_st.send_robust(sender=self)


if __name__ == "__main__":
    pass
