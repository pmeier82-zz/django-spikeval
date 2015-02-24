# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, View

from djspikeval.forms import TrialForm
from djspikeval.util import render_to

__all__ = [
    "TrialBaseView", "TrialCreate", "TrialDetail", "TrialUpdate", "TrialDelete",
    "TrialValidate"]
__author__ = "pmeier82"

Benchmark = apps.get_registered_model("djspikeval", "benchmark")
Trial = apps.get_registered_model("djspikeval", "trial")


class TrialBaseView(object):
    model = Trial


class TrialCreate(TrialBaseView, CreateView):
    template_name = "djspikeval/trial/create.html"
    form_class = TrialForm

    def get_form_kwargs(self):
        kwargs = super(TrialCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["benchmark"] = Benchmark.objects.get(pk=self.kwargs["pk"])
        return kwargs

    def get_success_url(self):
        if self.object is not None:
            return self.object.get_absolute_url()
        return reverse_lazy(self.kwargs["benchmark"])


class TrialDetail(TrialBaseView, DetailView):
    template_name = "djspikeval/trial/detail.html"

    def get_context_data(self, **kwargs):
        return super(TrialDetail, self).get_context_data(**kwargs)


class TrialUpdate(TrialBaseView, UpdateView):
    template_name = "djspikeval/trial/update.html"
    form_class = TrialForm

    def get_form_kwargs(self):
        kwargs = super(TrialUpdate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        if self.object is not None:
            return self.object.get_absolute_url()
        # return reverse_lazy("benchmark:list")
        return reverse_lazy(self.kwargs["benchmark"])


class TrialDelete(TrialBaseView, DeleteView):
    template_name = "djspikeval/trial/delete.html"

    def get_context_data(self, **kwargs):
        self.benchmark = self.object.benchmark
        return super(TrialDelete, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy(self.object.benchmark)


class TrialValidate(TrialBaseView, View):
    def get(self, response, *args, **kwargs):
        try:
            obj = get_object_or_404(Trial, pk=self.kwargs["pk"])
            assert obj.benchmark.is_accessible(self.request.user), "insufficient permissions"
            obj.validate()
            messages.info(self.request, "Validation run has been scheduled: %s" % obj)
        except Exception, ex:
            messages.error(self.request, "Validation run not scheduled: %s" % ex)
        finally:
            return redirect(self.kwargs.get("dest", obj))


if __name__ == "__main__":
    pass
