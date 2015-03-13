# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, View

from djspikeval.forms import DatafileForm
from djspikeval.util import render_to

__all__ = [
    "DatafileBaseView", "DatafileCreate", "DatafileDetail", "DatafileUpdate", "DatafileDelete", "DatafileValidate"]
__author__ = "pmeier82"

Benchmark = apps.get_registered_model("djspikeval", "dataset")
Trial = apps.get_registered_model("djspikeval", "datafile")


class DatafileBaseView(object):
    model = Trial


class DatafileCreate(DatafileBaseView, CreateView):
    template_name = "djspikeval/datafile/create.html"
    form_class = DatafileForm

    def get_form_kwargs(self):
        kwargs = super(DatafileCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["dataset"] = get_object_or_404(Benchmark, pk=self.kwargs["pk"])
        return kwargs

    def get_success_url(self):
        if self.object is not None:
            return self.object.get_absolute_url()
        return reverse_lazy(self.kwargs["dataset"])


class DatafileDetail(DatafileBaseView, DetailView):
    template_name = "djspikeval/datafile/detail.html"

    def get_context_data(self, **kwargs):
        return super(DatafileDetail, self).get_context_data(**kwargs)


class DatafileUpdate(DatafileBaseView, UpdateView):
    template_name = "djspikeval/datafile/update.html"
    form_class = DatafileForm

    def get_form_kwargs(self):
        kwargs = super(DatafileUpdate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        if self.object is not None:
            return self.object.get_absolute_url()
        return reverse_lazy(self.kwargs["dataset"])


class DatafileDelete(DatafileBaseView, DeleteView):
    template_name = "djspikeval/datafile/delete.html"

    def get_success_url(self):
        return reverse_lazy(self.object.dataset)


class DatafileValidate(DatafileBaseView, View):
    def get(self, response, *args, **kwargs):
        try:
            obj = get_object_or_404(Trial, pk=self.kwargs["pk"])
            assert obj.dataset.is_accessible(self.request.user), "insufficient permissions"
            obj.validate()
            messages.info(self.request, "Validation run has been scheduled: %s" % obj)
        except Exception, ex:
            messages.error(self.request, "Validation run not scheduled: %s" % ex)
        finally:
            return redirect(self.kwargs.get("dest", obj))


if __name__ == "__main__":
    pass
