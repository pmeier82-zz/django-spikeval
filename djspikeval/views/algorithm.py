# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from djspikeval.forms import AlgorithmForm
from djspikeval.util import render_to

__all__ = [
    "AlgorithmBaseView", "AlgorithmList", "AlgorithmCreate", "AlgorithmDetail",
    "AlgorithmUpdate", "AlgorithmDelete"]
__author__ = "pmeier82"

Algorithm = apps.get_registered_model("djspikeval", "algorithm")


class AlgorithmBaseView(object):
    model = Algorithm


class AlgorithmList(AlgorithmBaseView, ListView):
    template_name = "djspikeval/algorithm/list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        cntx = super(AlgorithmList, self).get_context_data(**kwargs)
        cntx.update(scope=self.request.GET.get("scope"))
        return cntx

    def get_queryset(self):
        if self.request.GET.get("scope"):
            scope = self.request.GET.get("scope")
            return Algorithm.objects.filter(
                Q(name__icontains=scope) |
                Q(kind__name__icontains=scope))
        return Algorithm.objects.all()


class AlgorithmCreate(AlgorithmBaseView, CreateView):
    template_name = "djspikeval/algorithm/create.html"
    form_class = AlgorithmForm

    def get_form_kwargs(self):
        kwargs = super(AlgorithmCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AlgorithmDetail(AlgorithmBaseView, DetailView):
    template_name = "djspikeval/algorithm/detail.html"


class AlgorithmUpdate(AlgorithmBaseView, UpdateView):
    template_name = "djspikeval/algorithm/update.html"
    form_class = AlgorithmForm

    def get_form_kwargs(self):
        kwargs = super(AlgorithmUpdate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AlgorithmDelete(AlgorithmBaseView, DeleteView):
    template_name = "djspikeval/algorithm/delete.html"
    success_url = reverse_lazy("algorithm:list")


if __name__ == "__main__":
    pass
