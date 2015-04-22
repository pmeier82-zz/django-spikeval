# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.apps import apps
from .util import form_with_captcha

__all__ = ["AlgorithmForm"]
__author__ = "pmeier82"

Algorithm = apps.get_registered_model("djspikeval", "algorithm")


@form_with_captcha
class AlgorithmForm(forms.ModelForm):
    """`Algorithm` model form"""

    # meta
    class Meta:
        model = Algorithm

    # constructor
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(AlgorithmForm, self).__init__(*args, **kwargs)
        if self.instance.id is None:
            self.fields.pop("user")
            self.instance.user = user


if __name__ == "__main__":
    pass
