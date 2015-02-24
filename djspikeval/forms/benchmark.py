# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.apps import apps
from util import form_with_captcha

__all__ = ["BenchmarkForm", "BenchmarkSearchForm"]
__author__ = "pmeier82"

Benchmark = apps.get_registered_model("djspikeval", "benchmark")


class BenchmarkForm(forms.ModelForm):
    """`Benchmark` model form"""

    # meta
    class Meta:
        model = Benchmark
        exclude = ("created", "modified", "status_changed", "modules")

    # constructor
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(BenchmarkForm, self).__init__(*args, **kwargs)
        if self.instance.id is None:
            self.fields.pop("status")
            self.fields.pop("owner")

    # interface
    def save(self, *args, **kwargs):
        if self.instance.id is None:
            if self.user is not None:
                self.instance.owner = self.user
        return super(BenchmarkForm, self).save(*args, **kwargs)


class BenchmarkSearchForm(forms.Form):
    """`Benchmark` search form"""

    name = forms.CharField(required=False)


if __name__ == "__main__":
    pass
