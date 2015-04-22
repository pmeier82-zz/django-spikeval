# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.apps import apps
from .util import form_with_captcha

__all__ = ["DatasetForm"]
__author__ = "pmeier82"

Dataset = apps.get_model("djspikeval", "dataset")
Module = apps.get_model("djspikeval", "module")


@form_with_captcha
class DatasetForm(forms.ModelForm):
    """`Dataset` model form"""

    # meta
    class Meta:
        model = Dataset
        exclude = ("created", "modified", "status_changed", "modules")

    # constructor
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(DatasetForm, self).__init__(*args, **kwargs)
        if self.instance.id is None:
            self.fields.pop("status")
            self.fields.pop("user")

    # interface
    def save(self, *args, **kwargs):
        if self.instance.id is None:
            if self.user is not None:
                self.instance.user = self.user
        return super(DatasetForm, self).save(*args, **kwargs)


class DatasetModuleForm(forms.ModelForm):
    """`Dataset` 2 `Module` form"""

    # meta
    class Meta:
        model = Dataset
        exclude = "__all__"

    modules = forms.ModelMultipleChoiceField(queryset=Module.objects.all())

    def save(self, commit=True):
        super(DatasetModuleForm, self).save(commit=commit)


if __name__ == "__main__":
    pass
