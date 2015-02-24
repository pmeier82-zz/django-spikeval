# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.apps import apps

__all__ = ["AlgorithmForm"]
__author__ = "pmeier82"

Algorithm = apps.get_registered_model("djspikeval", "algorithm")


class AlgorithmForm(forms.ModelForm):
    class Meta:
        model = Algorithm

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(AlgorithmForm, self).__init__(*args, **kwargs)
        if self.instance.id is None:
            self.fields.pop("owner")

    def save(self, *args, **kwargs):
        if self.user is not None:
            self.instance.owner = self.user
        return super(AlgorithmForm, self).save(*args, **kwargs)


if __name__ == "__main__":
    pass
