# -*- coding: utf-8 -*-

from django import forms
from django.apps import apps
from util import form_with_captcha

__author__ = "pmeier82"

Trial = apps.get_registered_model("djspikeval", "trial")
Batch = apps.get_registered_model("djspikeval", "batch")
Datafile = apps.get_registered_model("djspikeval", "datafile")
Evaluation = apps.get_registered_model("djspikeval", "evaluation")


class BatchEditForm(forms.ModelForm):
    class Meta:
        model = Batch
        exclude = ('status', 'status_changed', 'benchmark')


@form_with_captcha
class BatchSubmitForm(forms.ModelForm):
    class Meta:
        model = Batch
        exclude = ('owner', 'status', 'status_changed', 'benchmark')

    ## constructor

    def __init__(self, *args, **kwargs):
        self.benchmark = kwargs.pop('benchmark')
        super(BatchSubmitForm, self).__init__(*args, **kwargs)
        self.sub_ids = []
        for tr in self.benchmark.trial_set_valid():
            self.sub_ids.append('sub-tr-%s' % tr.id)
            self.fields['sub-tr-%s' % tr.id] = forms.FileField(
                label='Upload Trial: %s' % tr.name,
                required=False)

    def save(self, *args, **kwargs):
        # init and checks
        user = kwargs.pop('user')

        # build instance
        self.instance.owner = user
        self.instance.benchmark = self.benchmark
        self.instance.status = Batch.STATUS.private
        bt = super(BatchSubmitForm, self).save(*args, **kwargs)

        # evaluations
        for sub_id in self.sub_ids:
            if not self.cleaned_data[sub_id]:
                continue

            # evaluation
            pk = int(sub_id.split('-')[-1])
            tr = Trial.objects.get(id=pk)
            ev = Evaluation(batch=bt, trial=tr)
            ev.save()

            # datafile
            ev_file = Datafile(
                name=self.cleaned_data[sub_id].name,
                file=self.cleaned_data[sub_id],
                kind='st_file',
                content_object=ev)
            ev_file.save()
            ev.validate()

            # trigger evaluation
            ev.run()
        return bt


if __name__ == "__main__":
    pass
