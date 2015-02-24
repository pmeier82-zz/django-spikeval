# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.apps import apps
from util import form_with_captcha

__all__ = ["SubmissionForm"]
__author__ = "pmeier82"

Trial = apps.get_registered_model("djspikeval", "trial")
Evaluation = apps.get_registered_model("djspikeval", "evaluation")
Submission = apps.get_registered_model("djspikeval", "submission")


@form_with_captcha
class SubmissionForm(forms.ModelForm):
    """`Submission` model form"""

    # meta
    class Meta:
        model = Submission
        exclude = ("owner", "status", "status_changed", "benchmark")

    # constructor
    def __init__(self, *args, **kwargs):
        self.benchmark = kwargs.pop("benchmark")
        self.user = kwargs.pop("user")
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.sub_ids = []
        for trial in self.benchmark.trial_set_valid():
            self.sub_ids.append("sub-trial-%s".format(trial.id))
            self.fields["sub-trial-%s".format(trial.id)] = forms.FileField(
                label="Upload Trial: %s".format(trial.name),
                required=False)

    def save(self, *args, **kwargs):
        self.instance.owner = self.user
        self.instance.benchmark = self.benchmark
        self.instance.status = Submission.STATUS.private
        submission = super(SubmissionForm, self).save(*args, **kwargs)

        # evaluations
        for sub_id in self.sub_ids:
            if not self.cleaned_data[sub_id]:
                continue

            # evaluation
            pk = int(sub_id.split('-')[-1])
            trial = Trial.objects.get(id=pk)
            evalu = Evaluation(batch=submission, trial=trial)
            evalu.save()

            # TODO: finish!
            # # datafile
            # ev_file = Data(
            # name=self.cleaned_data[sub_id].name,
            # file=self.cleaned_data[sub_id],
            # kind='st_file',
            # content_object=evalu)
            # ev_file.save()
            # evalu.validate()

            # trigger evaluation
            evalu.run()
        return submission


if __name__ == "__main__":
    pass
