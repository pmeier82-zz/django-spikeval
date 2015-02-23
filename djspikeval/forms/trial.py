# -*- coding: utf-8 -*-

from django import forms
from django.apps import apps

__all__ = ["TrialForm"]
__author__ = "pmeier82"

Benchmark = apps.get_registered_model("djspikeval", "benchmark")
Datafile = apps.get_registered_model("djspikeval", "datafile")
Trial = apps.get_registered_model("djspikeval", "trial")


class TrialForm(forms.ModelForm):
    class Meta:
        model = Trial
        exclude = ("created", "modified", "valid_rd_log", "valid_gt_log")

    # extra fields
    rd_upload = forms.FileField(label='Rawdata File', required=False)
    gt_upload = forms.FileField(label='Groundtruth File', required=False)

    # constructor
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.benchmark = kwargs.pop("benchmark", None)
        super(TrialForm, self).__init__(*args, **kwargs)
        if self.instance.id is None:
            self.fields.pop("benchmark")
            self.initial["benchmark"] = self.benchmark
        if self.instance.rd_file:
            self.initial["rd_upload"] = self.instance.rd_file.data
        if self.instance.gt_file:
            self.initial["gt_upload"] = self.instance.gt_file.data
        if self.benchmark is not None:
            self.fields["parameter"].label = self.benchmark.parameter

    def save(self, *args, **kwargs):
        # init and checks
        if not self.changed_data:
            return
        if self.instance.id is None:
            if "rd_upload" not in self.changed_data:
                return
            self.instance.benchmark = self.benchmark
        tr = super(TrialForm, self).save(*args, **kwargs)

        # handling rd_file upload
        if "rd_upload" in self.changed_data:
            if tr.rd_file:
                tr.rd_file.delete()
                tr.valid_rd_log = None
                tr.save()
            if self.cleaned_data["rd_upload"]:
                rd_file = Datafile(
                    name=self.cleaned_data["rd_upload"].name,
                    data=self.cleaned_data["rd_upload"],
                    kind="rd_file",
                    content_object=tr)
                rd_file.save()

        # handling st_file upload
        if "gt_upload" in self.changed_data:
            if tr.gt_file:
                tr.gt_file.delete()
                tr.valid_gt_log = None
                tr.save()
            if self.cleaned_data["gt_upload"]:
                st_file = Datafile(
                    name=self.cleaned_data["gt_upload"].name,
                    data=self.cleaned_data["gt_upload"],
                    kind="st_file",
                    content_object=tr)
                st_file.save()

        # return
        return tr


if __name__ == "__main__":
    pass
