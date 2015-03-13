# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

__all__ = ["Module"]


class Module(TimeStampedModel):
    """djspikeval module

    modules are evaluation components that produce a partial evaluation result
    """

    # meta
    class Meta:
        app_label = "djspikeval"
        unique_together = ("name", "version")

    # fields
    name = models.CharField(
        max_length=255,
        blank=False)
    version = models.CharField(
        max_length=32,
        default="0.1")
    path = models.CharField(
        max_length=255,
        unique=True,
        blank=False)
    enabled = models.BooleanField(
        default=True)
    description = models.TextField(
        blank=True)
    dataset = models.ManyToManyField(
        "djspikeval.Dataset",
        blank=True,
        null=True)
    parent = models.ForeignKey(
        "self",
        related_name="children",
        blank=True,
        null=True)

    # managers
    asset_set = GenericRelation("base.Asset")

    @property
    def attachment_set(self):
        return self.asset_set.filter(kind="attachment")

    # methods
    def __unicode__(self):
        return unicode("Module: {} ({})".format(self.name, self.version))


if __name__ == "__main__":
    pass
