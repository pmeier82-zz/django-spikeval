# -*- coding: utf-8 -*-

from django.apps import apps

Asset = apps.get_registered_model("base", "asset")

__all__ = ["Attachment", "Datafile"]
__author__ = "pmeier82"


class Attachment(Asset):
    """`BaseFile` for attachments"""

    class Meta:
        proxy = True
        app_label = "djspikeval"

    UPLOAD_TO = "attachment"


class Datafile(Asset):
    """`BaseFile` for datafiles"""

    class Meta:
        proxy = True
        app_label = "djspikeval"

    UPLOAD_TO = "datafile"


if __name__ == "__main__":
    pass
