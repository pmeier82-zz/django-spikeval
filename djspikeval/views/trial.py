# -*- coding: utf-8 -*-

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from djspikeval.forms import TrialForm
from djspikeval.util import render_to


__author__ = "pmeier82"

Benchmark = apps.get_registered_model("djspikeval", "benchmark")
Trial = apps.get_registered_model("djspikeval", "trial")
# Module = apps.get_registered_model('spike', 'module')


@render_to("djspikeval/benchmark/trial.html")
def detail(request, pk):
    """renders details of a trial"""

    # init and checks
    try:
        tr = Trial.objects.get(pk=pk)
        assert tr.benchmark.has_access(request.user), 'insufficient permissions!'
    except Exception, ex:
        messages.error(request, 'You are not allowed to view or modify this Trial: %s' % ex)
        return redirect('bm_list')
    tr_form = None

    # post request
    if request.method == 'POST':
        if 'tr_edit' in request.POST:
            tr_form = TrialForm(data=request.POST, files=request.FILES, instance=tr)
            if tr_form.is_valid():
                if tr_form.save():
                    messages.success(request, 'Trial edit successful')
                else:
                    messages.info(request, 'No changes detected')
            else:
                messages.error(request, 'Trial edit failed')

    # create forms
    if not tr_form:
        tr_form = TrialForm(instance=tr, benchmark=tr.benchmark)

    # response
    return {'tr': tr,
            'tr_form': tr_form}


@login_required
def delete(request, pk, dest=None):
    """delete trial"""

    tr, bm = None, None
    try:
        tr = Trial.objects.get(pk=pk)
        bm = tr.benchmark
        assert tr.benchmark.has_access(request.user), 'insufficient permissions'
        Trial.objects.get(pk=pk).delete()
        messages.success(request, 'Trial "%s" deleted' % tr)
    except Exception, ex:
        messages.error(request, 'Trial not deleted: %s' % ex)
    finally:
        return redirect(dest or bm)


@login_required
def validate(request, pk, dest=None):
    try:
        tr = Trial.objects.get(pk=pk)
        assert tr.benchmark.has_access(request.user), 'insufficient permissions'
        tr.validate()
        messages.info(request, 'Validation run has been scheduled: %s' % tr)
    except Exception, ex:
        messages.error(request, 'Validation run not scheduled: %s' % ex)
    finally:
        return redirect(dest or tr)


# CLASS BASED VIEWS

class TrialBaseView(object):
    model = Trial


class TrialCreate(TrialBaseView, CreateView):
    template_name = "djspikeval/trial/create.html"
    form_class = TrialForm

    def get_form_kwargs(self):
        kwargs = super(TrialCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["benchmark"] = Benchmark.objects.get(pk=self.kwargs["pk"])
        # TODO insert benchmark
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()


class TrialDetail(TrialBaseView, DetailView):
    template_name = "djspikeval/trial/detail.html"


class TrialUpdate(TrialBaseView, UpdateView):
    template_name = "djspikeval/trial/update.html"
    form_class = TrialForm

    def get_form_kwargs(self):
        kwargs = super(TrialUpdate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TrialDelete(TrialBaseView, DeleteView):
    template_name = "djspikeval/trial/delete.html"
    success_url = reverse_lazy("trial:delete")


if __name__ == "__main__":
    pass
