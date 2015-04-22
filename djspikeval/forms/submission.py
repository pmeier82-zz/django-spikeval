# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.apps import apps
from django.forms import inlineformset_factory
from .util import form_with_captcha

__all__ = ["SubmissionForm"]
__author__ = "pmeier82"

Algorithm = apps.get_registered_model("djspikeval", "algorithm")
Analysis = apps.get_registered_model("djspikeval", "analysis")
Asset = apps.get_registered_model("base", "asset")
Datafile = apps.get_registered_model("djspikeval", "datafile")
Submission = apps.get_registered_model("djspikeval", "submission")


@form_with_captcha
class SubmissionForm(forms.ModelForm):
    """`Submission` model form"""

    # meta
    class Meta:
        model = Submission
        exclude = ("user", "status", "status_changed", "dataset")

    # constructor
    def __init__(self, *args, **kwargs):
        dataset = kwargs.pop("dataset", None)
        user = kwargs.pop("user", None)
        super(SubmissionForm, self).__init__(*args, **kwargs)
        if self.instance.id is None:
            self.instance.user = user
            self.instance.dataset = dataset
            self.instance.status = Submission.STATUS.private
        self.sub_form_ids = []
        for df in self.instance.dataset.datafile_set_valid():
            self.sub_form_ids.append("sub-datafile-{}".format(df.id))
            self.fields["sub-datafile-{}".format(df.id)] = forms.FileField(
                label="Upload: {}".format(df.name),
                required=False)

    def save(self, *args, **kwargs):
        sub = super(SubmissionForm, self).save(*args, **kwargs)

        # evaluations
        for sub_form_id in self.sub_form_ids:
            if sub_form_id in self.changed_data:
                # analysis
                pk = int(sub_form_id.split('-')[-1])
                datafile = Datafile.objects.get(id=pk)
                ana = Analysis(submission=sub, datafile=datafile)
                ana.save()

                # datafile
                st_file = Asset(
                    name=self.cleaned_data[sub_form_id].name,
                    data_orig_name=self.cleaned_data[sub_form_id].name,
                    data=self.cleaned_data[sub_form_id],
                    kind="st_file",
                    content_object=ana)
                st_file.save()
                ana.validate()

                # trigger analysis
                ana.start()
        return sub


if __name__ == "__main__":
    pass
