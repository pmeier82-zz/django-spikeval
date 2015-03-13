# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.apps import apps
from django.forms import inlineformset_factory
from util import form_with_captcha

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
        self.dataset = kwargs.pop("dataset", )
        self.user = kwargs.pop("user")
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.sub_form_ids = []
        for df in self.dataset.datafile_set_valid():
            self.sub_form_ids.append("sub-datafile-{}".format(df.id))
            self.fields["sub-datafile-{}".format(df.id)] = forms.FileField(
                label="Upload: {}".format(df.name),
                required=False)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        self.instance.dataset = self.dataset
        self.instance.status = Submission.STATUS.private
        sub = super(SubmissionForm, self).save(*args, **kwargs)

        # evaluations
        for sub_form_id in self.sub_form_ids:
            if not self.cleaned_data[sub_form_id]:
                continue

            # analysis
            pk = int(sub_form_id.split('-')[-1])
            datafile = Datafile.objects.get(id=pk)
            ana = Analysis(submission=sub, datafile=datafile)
            ana.save()

            # TODO: finish!
            # # datafile
            # ev_file = Data(
            # name=self.cleaned_data[sub_id].name,
            # file=self.cleaned_data[sub_id],
            # kind='st_file',
            # content_object=evalu)
            # ev_file.save()
            # evalu.validate()

            # trigger analysis
            ana.run()
        return sub


if __name__ == "__main__":
    pass
