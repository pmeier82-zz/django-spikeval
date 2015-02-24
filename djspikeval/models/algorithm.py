# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

__all__ = ["Algorithm"]
__author__ = "pmeier82"


class Algorithm(TimeStampedModel):
    """algorithm model"""

    # meta
    class Meta:
        app_label = "djspikeval"
        get_latest_by = "modified"
        ordering = ("-modified", "name", "version")
        unique_together = ("name", "version")

    # fields
    name = models.CharField(
        max_length=255,
        blank=False)
    version = models.CharField(
        max_length=32,
        default="0.1")
    description = models.TextField(
        blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=None,
        blank=True)
    parent = models.ForeignKey(
        "self",
        related_name="children",
        blank=True,
        null=True)

    # managers
    kind = TaggableManager(
        _("Algorithm Kind"),
        help_text="A comma-separated list of tags classifying the Algorithm.",
        blank=True)
    attachment_set = GenericRelation("djspikeval.Attachment")

    # methods
    def __unicode__(self):
        return unicode("{} ({})".format(self.name, self.version))

    @models.permalink
    def get_absolute_url(self):
        return "algorithm:detail", (self.pk,), {}

    @models.permalink
    def get_delete_url(self):
        return "algorithm:delete", (self.pk,), {}

    def has_access(self, user):
        return self.owner == user or getattr(user, "is_superuser", False) is True


if __name__ == "__main__":
    pass
