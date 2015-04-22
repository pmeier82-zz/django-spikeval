# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.apps import apps
from .util import form_with_captcha

__all__ = ["AttachmentForm"]
__author__ = "pmeier82"

Asset = apps.get_registered_model("base", "asset")


@form_with_captcha
class AttachmentForm(forms.ModelForm):
    """`Attachment` model form"""

    # meta
    class Meta:
        model = Asset
        fields = ("name", "data")

    # constructor
    def __init__(self, *args, **kwargs):
        obj = kwargs.pop("obj", None)
        if obj is None:
            raise ValueError("no related object passed!")
        super(AttachmentForm, self).__init__(*args, **kwargs)
        if self.instance.id is None:
            self.instance.kind = "attachment"
            self.instance.content_object = obj


if __name__ == "__main__":
    pass
