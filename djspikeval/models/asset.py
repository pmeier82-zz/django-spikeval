# -*- coding: utf-8 -*-

from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

Asset = apps.get_registered_model("base", "asset")

__all__ = ["Attachment", "Datafile"]
__author__ = "pmeier82"


class Attachment(Asset):
    """`BaseFile` for attachments"""

    class Meta:
        proxy = True
        app_label = "djspikeval"

    UPLOAD_PATH = "attachment"


class Datafile(Asset):
    """`BaseFile` for datafiles"""

    class Meta:
        proxy = True
        app_label = "djspikeval"

    UPLOAD_PATH = "datafile"


if __name__ == "__main__":
    pass
