# -*- coding: utf-8 -*-

from django import forms
from django.apps import apps

from util import form_with_captcha


__author__ = "pmeier82"

Benchmark = apps.get_registered_model("djspikeval", "benchmark")
Trial = apps.get_registered_model("djspikeval", "trial")
Batch = apps.get_registered_model("djspikeval", "batch")
Evaluation = apps.get_registered_model("djspikeval", "evaluation")


class BenchmarkForm(forms.ModelForm):
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


class BatchEditForm(forms.ModelForm):
    class Meta:
        model = Batch
        exclude = ("status", "status_changed", "benchmark")


@form_with_captcha
class BatchSubmitForm(forms.ModelForm):
    class Meta:
        model = Batch
        exclude = ("owner", "status", "status_changed", "benchmark")

    def __init__(self, *args, **kwargs):
        self.benchmark = kwargs.pop("benchmark")
        self.user = kwargs.pop("user")
        super(BatchSubmitForm, self).__init__(*args, **kwargs)
        self.sub_ids = []
        for trial in self.benchmark.trial_set_valid():
            self.sub_ids.append("sub-trial-%s".format(trial.id))
            self.fields["sub-trial-%s".format(trial.id)] = forms.FileField(
                label="Upload Trial: %s".format(trial.name),
                required=False)

    def save(self, *args, **kwargs):
        self.instance.owner = self.user
        self.instance.benchmark = self.benchmark
        self.instance.status = Batch.STATUS.private
        batch = super(BatchSubmitForm, self).save(*args, **kwargs)

        # evaluations
        for sub_id in self.sub_ids:
            if not self.cleaned_data[sub_id]:
                continue

            # evaluation
            pk = int(sub_id.split('-')[-1])
            trial = Trial.objects.get(id=pk)
            evalu = Evaluation(batch=batch, trial=trial)
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
        return batch


if __name__ == "__main__":
    pass
