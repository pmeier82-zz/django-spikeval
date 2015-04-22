# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _
from django.utils import importlib
from model_utils.models import TimeStampedModel
from model_utils.managers import InheritanceManager
from .dataset import Dataset

__all__ = ["Module"]


class Module(TimeStampedModel):
    """djspikeval module

    `Modules` are evaluation components that produce partial evaluation results. This entity is
     the glue between `djspikeval` and `spikeval` as it will load the `spikeval` modules into
     django context for execution.
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
        blank=False,
        default="0.1")
    module_path = models.CharField(
        max_length=255,
        blank=False,
        default="None")
    enabled = models.BooleanField(
        default=True)
    description = models.TextField(
        blank=True)
    dataset_set = models.ManyToManyField(
        Dataset,
        blank=True,
        null=True,
        related_name="module_set")
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

    # interface
    def get_module_cls(self):
        try:
            module_pkg = importlib.import_module(self.module_path)
            return module_pkg.Module
        except ImportError:
            return None

    def get_result_template(self):
        return "{}/result.html".format(self.module_path)


if __name__ == "__main__":
    pass
