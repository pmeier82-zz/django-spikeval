# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

__all__ = ["Submission"]
__author__ = "pmeier82"


class Submission(StatusModel, TimeStampedModel):
    """container for a set of evaluations submitted by a user for one dataset"""

    # meta
    class Meta:
        app_label = "djspikeval"

    # choices
    STATUS = Choices("private", "public")

    # fields
    description = models.TextField(
        blank=True,
        null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        help_text="The user associated with this submission.")
    algorithm = models.ForeignKey(
        "djspikeval.Algorithm",
        default=1,
        help_text="The Algorithm associated with this submission.")
    dataset = models.ForeignKey(
        "djspikeval.Dataset",
        help_text="The Dataset associated with this submission.",
        related_name="submission_set")

    # managers
    asset_set = GenericRelation("base.Asset")

    @property
    def attachment_set(self):
        return self.asset_set.filter(kind="attachment")

    # methods
    def __unicode__(self):
        return "#{} {} @{}".format(self.pk, self.algorithm, self.dataset)

    @models.permalink
    def get_absolute_url(self):
        return "analysis:detail", (self.pk,), {}

    @models.permalink
    def get_delete_url(self):
        return "analysis:delete", (self.pk,), {}

    def toggle(self):
        if self.status == self.STATUS.public:
            self.status = self.STATUS.private
        else:
            self.status = self.STATUS.public
        self.save()

    def is_public(self):
        return self.status == self.STATUS.public and self.dataset.is_public()

    def is_editable(self, user):
        return self.user == user or getattr(user, "is_superuser", False) is True

    def is_accessible(self, user):
        return self.is_public() or self.is_editable(user)


if __name__ == "__main__":
    pass
